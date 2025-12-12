// import React from 'react';
// import { Navigate, useLocation } from 'react-router-dom';
// import { useAuth } from '../contexts/AuthContext';

// interface ProtectedRouteProps {
//   children: React.ReactNode;
//   requiredRole?: 'admin' | 'user';
// }

// const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children, requiredRole }) => {
//   const { user, loading } = useAuth(); // Use 'loading' instead of 'isLoading'
//   const location = useLocation();
  
//   // Calculate isAuthenticated based on user existence
//   const isAuthenticated = !!user;

//   console.log('🛡️ ProtectedRoute check:', { 
//     isAuthenticated, 
//     userRole: user?.role, 
//     loading, // Use 'loading' instead of 'isLoading'
//     hasUser: !!user,
//     pathname: location.pathname
//   });

//   // Show spinner while auth is still loading (initial app load)
//   if (loading) { // Use 'loading' instead of 'isLoading'
//     return (
//       <div className="min-h-screen flex items-center justify-center bg-gray-50">
//         <div className="flex flex-col items-center">
//           <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
//           <span className="text-gray-600">Checking authentication...</span>
//         </div>
//       </div>
//     );
//   }

//   // Not logged in → redirect to login with return URL
//   if (!isAuthenticated) {
//     console.log('🚫 Not authenticated, redirecting to login');
//     return <Navigate to="/login" state={{ from: location }} replace />;
//   }

//   // Check if user account is activated
//   if (!user?.isActive) {
//     console.log('⏳ Account not activated, redirecting to activation notice');
//     return (
//       <div className="min-h-screen flex items-center justify-center bg-gray-50">
//         <div className="max-w-md w-full bg-white p-8 rounded-lg shadow-md text-center">
//           <div className="text-yellow-500 text-6xl mb-4">⚠️</div>
//           <h2 className="text-2xl font-bold text-gray-900 mb-2">Account Not Activated</h2>
//           <p className="text-gray-600 mb-4">
//             Please check your email and activate your account before accessing this page.
//           </p>
//           <div className="space-y-3">
//             <button
//               onClick={() => window.location.reload()}
//               className="block w-full bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-colors"
//             >
//               Check Again
//             </button>
//             <button
//               onClick={() => window.location.href = '/login'}
//               className="block w-full bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700 transition-colors"
//             >
//               Go to Login
//             </button>
//           </div>
//         </div>
//       </div>
//     );
//   }

//   // Role restriction check
//   if (requiredRole && user?.role !== requiredRole) {
//     console.log('⛔ Insufficient permissions, redirecting to home');
//     return (
//       <div className="min-h-screen flex items-center justify-center bg-gray-50">
//         <div className="max-w-md w-full bg-white p-8 rounded-lg shadow-md text-center">
//           <div className="text-red-500 text-6xl mb-4">🚫</div>
//           <h2 className="text-2xl font-bold text-gray-900 mb-2">Access Denied</h2>
//           <p className="text-gray-600 mb-4">
//             You don't have permission to access this page. Required role: {requiredRole}
//           </p>
//           <div className="space-y-3">
//             <button
//               onClick={() => window.location.href = '/'}
//               className="block w-full bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 transition-colors"
//             >
//               Go Home
//             </button>
//             <button
//               onClick={() => window.location.href = '/chat'}
//               className="block w-full bg-gray-600 text-white px-4 py-2 rounded hover:bg-gray-700 transition-colors"
//             >
//               Go to Chat
//             </button>
//           </div>
//         </div>
//       </div>
//     );
//   }

//   console.log('✅ Access granted to:', user?.role, 'user');
//   return <>{children}</>;
// };

// export default ProtectedRoute;