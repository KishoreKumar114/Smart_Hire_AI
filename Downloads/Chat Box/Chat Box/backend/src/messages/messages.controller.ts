import { Controller, Get, Post, Body, Param, UseGuards, Req } from '@nestjs/common';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';
import { MessagesService } from './messages.service';

@Controller('messages')
@UseGuards(JwtAuthGuard)
export class MessagesController {
  constructor(private readonly messagesService: MessagesService) {}

  // Get conversation between current user and another user
  @Get('conversation/:userId')
  async getConversation(@Req() req, @Param('userId') otherUserId: number) {
    return this.messagesService.getConversation(req.user.id, otherUserId);
  }

  // Get unread message counts
  @Get('unread-counts')
  async getUnreadCounts(@Req() req) {
    return this.messagesService.getUnreadCount(req.user.id);
  }

  // Mark messages as seen
  @Post('mark-seen/:senderId')
  async markMessagesAsSeen(@Req() req, @Param('senderId') senderId: number) {
    await this.messagesService.markMessagesAsSeen(senderId, req.user.id);
    return { success: true, message: 'Messages marked as seen' };
  }

  // Get last messages for all conversations
  @Get('last-messages')
  async getLastMessages(@Req() req) {
    return this.messagesService.getLastMessages(req.user.id);
  }
}