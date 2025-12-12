import { 
  Controller, 
  Get, 
  Post, 
  Body, 
  UseGuards, 
  Req,
  HttpException,
  HttpStatus,
  ConflictException
} from '@nestjs/common';
import { UsersService } from './users.service';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';

@Controller('users')
export class UsersController {
  constructor(private readonly usersService: UsersService) {}

  @Get()
  async findAll() {
    try {
      const users = await this.usersService.findAll();
      return users;
    } catch (error) {
      throw new HttpException('Failed to fetch users', HttpStatus.INTERNAL_SERVER_ERROR);
    }
  }

  @Get('profile')
  @UseGuards(JwtAuthGuard)
  async getProfile(@Req() req) {
    try {
      const user = await this.usersService.findById(req.user.id);
      if (!user) {
        throw new HttpException('User not found', HttpStatus.NOT_FOUND);
      }
      
      // Remove sensitive fields
      const { password, ...result } = user;
      return result;
    } catch (error) {
      throw new HttpException('Failed to fetch profile', HttpStatus.INTERNAL_SERVER_ERROR);
    }
  }

  // NEW: Get all users except current user (for contact list)
  @Get('all-except-me')
  @UseGuards(JwtAuthGuard)
  async getAllExceptMe(@Req() req) {
    try {
      const users = await this.usersService.findAllExceptCurrent(req.user.id);
      return users;
    } catch (error) {
      throw new HttpException('Failed to fetch users', HttpStatus.INTERNAL_SERVER_ERROR);
    }
  }

  // NEW: Get online users
  @Get('online')
  @UseGuards(JwtAuthGuard)
  async getOnlineUsers(@Req() req) {
    try {
      const onlineUsers = await this.usersService.getOnlineUsers();
      return onlineUsers;
    } catch (error) {
      throw new HttpException('Failed to fetch online users', HttpStatus.INTERNAL_SERVER_ERROR);
    }
  }

  // NEW: Set online/offline status
  @Post('set-online')
  @UseGuards(JwtAuthGuard)
  async setOnline(@Req() req, @Body() body: { isOnline: boolean }) {
    try {
      await this.usersService.setOnlineStatus(req.user.id, body.isOnline);
      return { success: true, isOnline: body.isOnline };
    } catch (error) {
      throw new HttpException('Failed to update online status', HttpStatus.INTERNAL_SERVER_ERROR);
    }
  }

  // Simple health check
  @Get('health')
  healthCheck() {
    return { 
      status: 'OK', 
      service: 'Users Service',
      timestamp: new Date().toISOString() 
    };
  }
}