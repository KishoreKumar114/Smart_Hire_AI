import React, { createContext, useState, useContext, useEffect } from 'react';
import type { ReactNode } from 'react'; 
import { authAPI } from '../service/api'; // ✅ Fixed import path
import { webSocketService } from '../service/websocket.service'; // NEW: WebSocket import
import type { User } from '../types';

// Define AuthContextType
interface AuthContextType {
  user: User | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  loading: boolean;
}

// Create Context
const AuthContext = createContext<AuthContextType | undefined>(undefined);

// AuthProvider Component
export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check for existing auth token on app load
    const checkAuth = async () => {
      try {
        const token = localStorage.getItem('token');
        const userData = localStorage.getItem('user');
        
        if (token && userData) {
          // Use stored user data
          const userObj = JSON.parse(userData);
          setUser(userObj);
          
          // NEW: Connect to WebSocket if user exists
          webSocketService.connect(token);
        }
      } catch (error) {
        console.error('Auth check error:', error);
        localStorage.removeItem('token');
        localStorage.removeItem('user');
      } finally {
        setLoading(false);
      }
    };

    checkAuth();
  }, []);

  const login = async (email: string, password: string) => {
    try {
      setLoading(true);
      console.log('🔐 Attempting login with:', { email });
      
      // ✅ Use authAPI instead of fetch
      const response = await authAPI.login({ email, password });
      console.log('✅ Login response:', response.data);

      if (response.data && response.data.user) {
        const userData: User = response.data.user;
        
        // Store user data and token
        setUser(userData);
        localStorage.setItem('user', JSON.stringify(userData));
        localStorage.setItem('token', response.data.access_token);
        
        // NEW: Connect to WebSocket after successful login
        webSocketService.connect(response.data.access_token);
        
        console.log('✅ User logged in successfully:', userData.name);
      } else {
        throw new Error('Invalid response from server');
      }
    } catch (error) {
      console.error('❌ Login error:', error);
      // Clear any partial auth data
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      setUser(null);
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const logout = () => {
    // NEW: Disconnect WebSocket first
    webSocketService.disconnect();
    
    setUser(null);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    console.log('🚪 User logged out');
  };

  const value: AuthContextType = {
    user,
    login,
    logout,
    loading
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to use auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};