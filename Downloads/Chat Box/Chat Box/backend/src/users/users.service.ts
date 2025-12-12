import { Injectable, ConflictException, InternalServerErrorException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { User } from './user.entity';
import * as bcrypt from 'bcryptjs';

@Injectable()
export class UsersService {
  constructor(
    @InjectRepository(User)
    private userRepository: Repository<User>,
  ) {}

  // Create simple user (no activation)
  async createSimpleUser(userData: { name: string; email: string; password: string }): Promise<User> {
    // Check if user already exists
    const existingUser = await this.userRepository.findOne({
      where: [
        { name: userData.name },
        { email: userData.email }
      ]
    });

    if (existingUser) {
      if (existingUser.name === userData.name) {
        throw new ConflictException('Username already exists');
      }
      if (existingUser.email === userData.email) {
        throw new ConflictException('Email already exists');
      }
    }

    try {
      // Hash password
      const hashedPassword = await bcrypt.hash(userData.password, 12);

      // Create user
      const user = this.userRepository.create({
        name: userData.name,
        email: userData.email,
        password: hashedPassword,
        isActive: true, // Auto-activate
      });

      return await this.userRepository.save(user);
    } catch (error) {
      console.error('User creation error:', error);
      throw new InternalServerErrorException('Failed to create user');
    }
  }

  // Find user by email
  async findByEmail(email: string): Promise<User | null> {
    return this.userRepository.findOne({ where: { email } });
  }

  // Find user by username
  async findByName(name: string): Promise<User | null> {
    return this.userRepository.findOne({ where: { name } });
  }

  // Find user by ID
  async findById(id: number): Promise<User | null> {
    return this.userRepository.findOne({ where: { id } });
  }

  // Update last login timestamp
  async updateLastLogin(userId: number): Promise<void> {
    await this.userRepository.update(userId, {
      lastLoginAt: new Date()
    });
  }

  // Get all users (for chat features)
  async findAll(): Promise<User[]> {
    return this.userRepository.find({
      select: ['id', 'name', 'email', 'role', 'isActive', 'isOnline', 'lastLoginAt', 'lastSeenAt', 'createdAt']
    });
  }

  // FIXED: Set user online status
  async setOnlineStatus(userId: number, isOnline: boolean): Promise<void> {
    if (isOnline) {
      // User came online - only update isOnline field
      await this.userRepository.update(userId, { 
        isOnline: true 
      });
    } else {
      // User went offline - update both isOnline and lastSeenAt
      await this.userRepository.update(userId, { 
        isOnline: false,
        lastSeenAt: new Date()
      });
    }
  }

  // FIXED: Get all users except current user
  // FIXED: Get all users except current user
async findAllExceptCurrent(userId: number): Promise<User[]> {
  return this.userRepository
    .createQueryBuilder('user')
    .select(['user.id', 'user.name', 'user.email', 'user.isOnline', 'user.lastSeenAt', 'user.createdAt'])
    .where('user.id != :userId', { userId })
    .getMany();
}

  // Get online users
  async getOnlineUsers(): Promise<User[]> {
    return this.userRepository.find({
      where: { isOnline: true },
      select: ['id', 'name', 'email', 'isOnline', 'lastSeenAt']
    });
  }

  // Get all users for contact list (excluding current user)
  async getContacts(userId: number): Promise<User[]> {
    return this.userRepository.find({
      where: { id: userId },
      select: ['id', 'name', 'email', 'isOnline', 'lastSeenAt', 'createdAt']
    });
  }
}