import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import { authAPI } from '../service/api'; // Fixed import path (services instead of service)

const ActivationPage: React.FC = () => {
  const { token } = useParams<{ token: string }>();
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading');
  const [message, setMessage] = useState('');

  useEffect(() => {
    const activateAccount = async () => {
      if (!token) {
        setStatus('error');
        setMessage('Invalid activation link. Please check your email and try again.');
        return;
      }

      try {
        console.log('🔐 Activating account with token:', token);
        const response = await authAPI.activate(token);
        
        // Check if activation was successful
        if (response.data && response.data.success) {
          setStatus('success');
          setMessage('Your account has been successfully activated! You can now sign in to your account.');
        } else {
          setStatus('error');
          setMessage(response.data?.message || 'Activation failed. Please try again.');
        }
      } catch (error: any) {
        console.error('Activation error:', error);
        setStatus('error');
        setMessage(
          error.response?.data?.message || 
          error.response?.data?.error ||
          'Activation failed. The link may have expired or is invalid.'
        );
      }
    };

    activateAccount();
  }, [token]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full bg-white p-8 rounded-lg shadow-md">
        <div className="text-center">
          {status === 'loading' && (
            <>
              <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-blue-600 mx-auto mb-4"></div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Activating Your Account</h2>
              <p className="text-gray-600">Please wait while we verify your account...</p>
            </>
          )}

          {status === 'success' && (
            <>
              <div className="text-green-500 text-6xl mb-4">✓</div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Welcome Aboard!</h2>
              <p className="text-gray-600 mb-6">{message}</p>
              <Link
                to="/login"
                className="inline-block bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700 transition duration-200 font-medium"
              >
                Sign In Now
              </Link>
            </>
          )}

          {status === 'error' && (
            <>
              <div className="text-red-500 text-6xl mb-4">⚠️</div>
              <h2 className="text-2xl font-bold text-gray-900 mb-2">Activation Issue</h2>
              <p className="text-gray-600 mb-6">{message}</p>
              <div className="space-y-3">
                <Link
                  to="/register"
                  className="block bg-blue-600 text-white px-6 py-3 rounded-md hover:bg-blue-700 transition duration-200 font-medium"
                >
                  Register Again
                </Link>
                <Link
                  to="/login"
                  className="block text-blue-600 hover:text-blue-500 font-medium"
                >
                  Back to Login
                </Link>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default ActivationPage;