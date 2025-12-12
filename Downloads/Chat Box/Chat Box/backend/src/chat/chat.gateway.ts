import {
  WebSocketGateway,
  WebSocketServer,
  SubscribeMessage,
  OnGatewayConnection,
  OnGatewayDisconnect,
} from '@nestjs/websockets';
import { Server, Socket } from 'socket.io';
import { JwtService } from '@nestjs/jwt';
import { MessagesService } from '../messages/messages.service';
import { UsersService } from '../users/users.service';

@WebSocketGateway({
  cors: {
    origin: ['http://localhost:5173', 'http://localhost:3000'],
    credentials: true,
  },
})
export class ChatGateway implements OnGatewayConnection, OnGatewayDisconnect {
  @WebSocketServer()
  server: Server;

  private connectedUsers: Map<number, string> = new Map(); // userId -> socketId

  constructor(
    private jwtService: JwtService,
    private messagesService: MessagesService,
    private usersService: UsersService,
  ) {}

  async handleConnection(client: Socket) {
    try {
      const token = client.handshake.auth.token;
      if (!token) {
        client.disconnect();
        return;
      }

      const payload = this.jwtService.verify(token);
      const userId = payload.sub;

      // Store user connection
      this.connectedUsers.set(userId, client.id);
      
      // Set user as online
      await this.usersService.setOnlineStatus(userId, true);
      
      // Notify all users about online status
      this.server.emit('user_online', { userId });
      
      console.log(`User ${userId} connected`);
    } catch (error) {
      console.error('WebSocket connection error:', error);
      client.disconnect();
    }
  }

  async handleDisconnect(client: Socket) {
    // Find user by socket ID and set offline
    for (const [userId, socketId] of this.connectedUsers.entries()) {
      if (socketId === client.id) {
        this.connectedUsers.delete(userId);
        await this.usersService.setOnlineStatus(userId, false);
        this.server.emit('user_offline', { userId });
        console.log(`User ${userId} disconnected`);
        break;
      }
    }
  }

  @SubscribeMessage('send_message')
  async handleSendMessage(client: Socket, payload: {
    content: string;
    receiverId: number;
    senderId: number;
  }) {
    try {
      // Save message to database
      const message = await this.messagesService.createMessage(
        payload.senderId,
        payload.receiverId,
        payload.content
      );

      // Send to receiver if online
      const receiverSocketId = this.connectedUsers.get(payload.receiverId);
      if (receiverSocketId) {
        this.server.to(receiverSocketId).emit('receive_message', message);
      }

      // Send back to sender for confirmation
      client.emit('message_sent', message);

      console.log(`Message sent from ${payload.senderId} to ${payload.receiverId}`);

    } catch (error) {
      console.error('Error sending message:', error);
      client.emit('message_error', { error: 'Failed to send message' });
    }
  }

  @SubscribeMessage('mark_messages_seen')
  async handleMarkMessagesSeen(client: Socket, payload: { senderId: number, receiverId: number }) {
    try {
      await this.messagesService.markMessagesAsSeen(payload.senderId, payload.receiverId);
      
      // Notify the sender that messages were seen
      const senderSocketId = this.connectedUsers.get(payload.senderId);
      if (senderSocketId) {
        this.server.to(senderSocketId).emit('messages_seen', { 
          seenBy: payload.receiverId,
          seenAt: new Date()
        });
      }

      console.log(`Messages from ${payload.senderId} marked as seen by ${payload.receiverId}`);

    } catch (error) {
      console.error('Error marking messages as seen:', error);
    }
  }

  @SubscribeMessage('typing_start')
  async handleTypingStart(client: Socket, payload: { senderId: number, receiverId: number }) {
    const receiverSocketId = this.connectedUsers.get(payload.receiverId);
    if (receiverSocketId) {
      this.server.to(receiverSocketId).emit('user_typing', { senderId: payload.senderId });
    }
  }

  @SubscribeMessage('typing_stop')
  async handleTypingStop(client: Socket, payload: { senderId: number, receiverId: number }) {
    const receiverSocketId = this.connectedUsers.get(payload.receiverId);
    if (receiverSocketId) {
      this.server.to(receiverSocketId).emit('user_stopped_typing', { senderId: payload.senderId });
    }
  }

  // Get online users
  @SubscribeMessage('get_online_users')
  async handleGetOnlineUsers(client: Socket) {
    try {
      const onlineUsers = await this.usersService.getOnlineUsers();
      client.emit('online_users', onlineUsers);
    } catch (error) {
      console.error('Error getting online users:', error);
    }
  }
}