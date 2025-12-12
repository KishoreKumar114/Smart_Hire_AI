// User and Auth Types
export interface User {
  id: number;
  email: string;
  name: string;
  role: 'admin' | 'user';
  isActive: boolean;
  isOnline: boolean;
  lastLoginAt?: string;
  createdAt: string;
}

export interface LoginFormData {
  email: string;
  password: string;
}

export interface RegisterFormData {
  email: string;
  name: string;
  password: string;
  confirmPassword: string;
}

export interface AuthResponse {
  access_token: string;
  user: User;
  message?: string;
}

export interface ApiError {
  message: string;
  statusCode: number;
}

// Activation flow
export interface ActivationRequest {
  token: string;
}

export interface ResendActivationRequest {
  email: string;
}

export interface ForgotPasswordRequest {
  email: string;
}

export interface ResetPasswordRequest {
  token: string;
  newPassword: string;
  confirmPassword: string;
}

// Chat Types
export interface ChatUser {
  id: number;
  name: string;
  createdAt: string;
}

export interface Message {
  id: number;
  content: string;
  sender: User;
  receiver: User;
  senderId: number;
  receiverId: number;
  isSeen: boolean; // NEW
  seenAt?: string;
  createdAt: string;
}

// Auth Context Type - Make sure this is exported
export interface AuthContextType {
  user: User | null;
  login: (userData: User) => void;
  logout: () => void;
  isAuthenticated: boolean;
}

export interface SendMessageData {
  content: string;
  receiverId: number;
  receiverName: string;
  senderId: number;
  senderName: string;
}

export interface WebSocketMessage {
  event: string;
  data: any;
}

export interface UnreadCounts {
  [key: number]: number;
}
export interface ChatContact {
  user: User;
  lastMessage?: Message;
  unreadCount: number;
}