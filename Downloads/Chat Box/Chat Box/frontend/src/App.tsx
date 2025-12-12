// src/App.tsx
import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';


// Components
// import ProtectedRoute from './components/ProtectedRoute';
import LoginForm from './components/LoginForm';
import RegisterForm from './components/RegisterForm';
import ActivationPage from './components/ActivationPage';
import ChatDashboard from './components/ChatDashboard';

// Simple Home component for authenticated users
const Home: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="max-w-md w-full bg-white p-8 rounded-lg shadow-md text-center">
        <h1 className="text-3xl font-bold text-gray-900 mb-4">Welcome to Chat App!</h1>
        <p className="text-gray-600 mb-6">
          You have successfully logged in to your account.
        </p>
        <div className="space-y-4">
          <p className="text-sm text-gray-500">
            This is a protected page that only authenticated users can access.
          </p>
          <div className="space-y-2">
            <a 
              href="/chat" 
              className="block w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 transition-colors"
            >
              Go to Chat
            </a>
            <a 
              href="/home" 
              className="block w-full bg-gray-600 text-white py-2 px-4 rounded-md hover:bg-gray-700 transition-colors"
            >
              Stay Here
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};

function App() {
  return (
    <div className="App">
      <Routes>
        {/* Public routes */}
        <Route path="/login" element={<LoginForm />} />
        <Route path="/register" element={<RegisterForm />} />
        <Route path="/activate/:token" element={<ActivationPage />} />
        
        {/* Redirect root to home */}
        <Route path="/" element={<Navigate to="/home" replace />} />

        {/* Protected routes */}
        <Route
          path="/home"
          element={
            // <ProtectedRoute>
              <Home />
            // </ProtectedRoute>
          }
        />

        <Route
          path="/chat"
          element={
            // <ProtectedRoute>
              <ChatDashboard />
            // </ProtectedRoute>
          }
        />
        
        {/* 404 fallback */}
        <Route path="*" element={
          <div className="min-h-screen flex items-center justify-center bg-gray-50">
            <div className="text-center">
              <h1 className="text-4xl font-bold text-gray-900 mb-4">404</h1>
              <p className="text-gray-600 mb-6">Page not found</p>
              <a 
                href="/home" 
                className="text-blue-600 hover:text-blue-500 font-medium"
              >
                Go Home
              </a>
            </div>
          </div>
        } />
      </Routes>
    </div>
  );
}

export default App;