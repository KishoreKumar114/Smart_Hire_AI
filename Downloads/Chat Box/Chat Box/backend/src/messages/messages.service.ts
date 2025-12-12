import { Injectable } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Message } from './message.entity';

@Injectable()
export class MessagesService {
  constructor(
    @InjectRepository(Message)
    private messageRepository: Repository<Message>,
  ) {}

  // Create new message
  async createMessage(senderId: number, receiverId: number, content: string): Promise<Message> {
    const message = this.messageRepository.create({
      senderId,
      receiverId,
      content,
      isSeen: false,
    });
    return await this.messageRepository.save(message);
  }

  // Get conversation between two users
  async getConversation(user1Id: number, user2Id: number): Promise<Message[]> {
    return this.messageRepository
      .createQueryBuilder('message')
      .where(
        '(message.senderId = :user1Id AND message.receiverId = :user2Id) OR (message.senderId = :user2Id AND message.receiverId = :user1Id)',
        { user1Id, user2Id }
      )
      .orderBy('message.createdAt', 'ASC')
      .getMany();
  }

  // Mark messages as seen
  async markMessagesAsSeen(senderId: number, receiverId: number): Promise<void> {
    await this.messageRepository
      .createQueryBuilder()
      .update(Message)
      .set({ 
        isSeen: true,
        seenAt: new Date()
      })
      .where('senderId = :senderId AND receiverId = :receiverId AND isSeen = false', {
        senderId,
        receiverId
      })
      .execute();
  }

  // Get unread message count for a user
  async getUnreadCount(userId: number): Promise<{ [key: number]: number }> {
    const results = await this.messageRepository
      .createQueryBuilder('message')
      .select('message.senderId, COUNT(*) as count')
      .where('message.receiverId = :userId AND message.isSeen = false', { userId })
      .groupBy('message.senderId')
      .getRawMany();

    const unreadCounts: { [key: number]: number } = {};
    results.forEach(result => {
      unreadCounts[result.senderId] = parseInt(result.count);
    });

    return unreadCounts;
  }

  // Get last message for each conversation
  async getLastMessages(userId: number): Promise<Message[]> {
    return this.messageRepository
      .createQueryBuilder('message')
      .where('message.senderId = :userId OR message.receiverId = :userId', { userId })
      .orderBy('message.createdAt', 'DESC')
      .getMany();
  }
}