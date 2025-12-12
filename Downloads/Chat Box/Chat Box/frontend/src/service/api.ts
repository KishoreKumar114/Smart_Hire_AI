import axios from 'axios';
import Cookies from 'js-cookie';

const API_BASE_URL = 'http://localhost:3001/api';

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,
  timeout: 10000,
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token') || localStorage.getItem('access_token') || Cookies.get('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
    console.log('🔐 Adding token to request:', config.url);
  }
  
  // Log all requests for debugging
  console.log(`🚀 API ${config.method?.toUpperCase()}: ${config.baseURL}${config.url}`);
  
  return config;
});

// Handle responses
api.interceptors.response.use(
  (response) => {
    console.log('✅ API Success:', response.config.url, response.status);
    return response;
  },
  (error) => {
    console.log('🔍 API Error Details:', {
      status: error.response?.status,
      url: error.config?.baseURL + error.config?.url,
      method: error.config?.method,
      message: error.message,
      data: error.response?.data
    });

    // Handle 401 only for specific cases
    if (error.response?.status === 401) {
      console.log('🛡️ 401 Unauthorized detected for:', error.config?.url);
      
      // ✅ ADD EXCEPTION FOR AUTH ENDPOINTS
      if (error.config?.url?.includes('/auth/login') || 
          error.config?.url?.includes('/auth/register') ||
          error.config?.url?.includes('/auth/activate')) {
        console.log('🛡️ Not logging out for auth endpoints 401');
        return Promise.reject(error);
      }

      // Remove tokens and redirect (only for protected endpoints)
      localStorage.removeItem('token');
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      Cookies.remove('access_token');
      Cookies.remove('user');
      
      // Only redirect if not already on login page
      if (!window.location.pathname.includes('/login')) {
        setTimeout(() => {
          window.location.href = '/login';
        }, 100);
      }
    }
    
    return Promise.reject(error);
  }
);

// ✅ AUTH ENDPOINTS
export const authAPI = {
  login: (credentials: { email: string; password: string }) => 
    api.post('/auth/login', credentials),
  
  register: (data: { name: string; email: string; password: string }) => 
    api.post('/auth/register', data),
  
  activate: (token: string) => 
    api.get(`/auth/activate/${token}`),
  
  getProfile: () => 
    api.get('/auth/profile'),
  
  logout: () => 
    api.post('/auth/logout'),
  
  health: () =>
    api.get('/auth/health')
};

// ✅ USERS API - With new contact features
export const usersApi = {
  getAllUsers: () =>
    api.get('/users'),
  
  getProfile: () =>
    api.get('/users/profile'),

  // NEW: Contact list features
  getOnlineUsers: () =>
    api.get('/users/online'),
  
  getAllUsersExceptMe: () =>
    api.get('/users/all-except-me'),
  
  setOnlineStatus: (isOnline: boolean) =>
    api.post('/users/set-online', { isOnline }),
};

// ✅ MESSAGES API - Enhanced with seen status and unread counts
export const messagesApi = {
  getConversation: (otherUserId: number) =>
    api.get(`/messages/conversation/${otherUserId}`),
  
  getUnreadCounts: () =>
    api.get('/messages/unread-counts'),
  
  markMessagesAsSeen: (senderId: number) =>
    api.post(`/messages/mark-seen/${senderId}`),
  
  getLastMessages: () =>
    api.get('/messages/last-messages'),
};

// ✅ Export for backward compatibility
export const usersAPI = authAPI;

export default api;