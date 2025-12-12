import { io, Socket } from 'socket.io-client';

// Define specific callback types
type EventCallback = (...args: any[]) => void;

class WebSocketService {
  private socket: Socket | null = null;
  private eventCallbacks: { [event: string]: EventCallback[] } = {};

  connect(token: string) {
    if (this.socket) {
      this.disconnect();
    }

    this.socket = io('http://localhost:3001', {
      auth: { token },
      transports: ['websocket'],
    });

    this.socket.on('connect', () => {
      console.log('✅ WebSocket connected');
    });

    this.socket.on('disconnect', () => {
      console.log('❌ WebSocket disconnected');
    });

    // Register all event listeners
    Object.keys(this.eventCallbacks).forEach(event => {
      this.eventCallbacks[event].forEach(callback => {
        this.socket?.on(event, callback);
      });
    });
  }

  disconnect() {
    if (this.socket) {
      this.socket.disconnect();
      this.socket = null;
    }
  }

  on(event: string, callback: EventCallback) {
    if (!this.eventCallbacks[event]) {
      this.eventCallbacks[event] = [];
    }
    this.eventCallbacks[event].push(callback);

    // If socket is already connected, register the event immediately
    if (this.socket) {
      this.socket.on(event, callback);
    }
  }

  off(event: string, callback: EventCallback) {
    if (this.eventCallbacks[event]) {
      this.eventCallbacks[event] = this.eventCallbacks[event].filter(cb => cb !== callback);
    }
    this.socket?.off(event, callback);
  }

  emit(event: string, data: any) {
    if (this.socket) {
      this.socket.emit(event, data);
    }
  }

  isConnected(): boolean {
    return this.socket?.connected || false;
  }
}

export const webSocketService = new WebSocketService();