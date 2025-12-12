import { Injectable, UnauthorizedException, BadRequestException, InternalServerErrorException, ConflictException } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import { UsersService } from '../users/users.service';
import { EmailService } from '../email/email.service';
import * as bcrypt from 'bcryptjs';

@Injectable()
export class AuthService {
  constructor(
    private usersService: UsersService,
    private jwtService: JwtService,
    private emailService: EmailService,
  ) {}

  // Validate credentials (no activation check)
  async validateUser(email: string, password: string): Promise<any> {
    const user = await this.usersService.findByEmail(email);

    if (!user) {
      throw new UnauthorizedException('Invalid email or password');
    }

    const isPasswordValid = await bcrypt.compare(password, user.password);
    if (!isPasswordValid) {
      throw new UnauthorizedException('Invalid email or password');
    }

    // Remove sensitive fields
    const { password: _, ...result } = user;
    return result;
  }

  // Login user
  async login(user: any) {
    // Update last login
    await this.usersService.updateLastLogin(user.id);

    const payload = {
      email: user.email,
      sub: user.id,
      role: user.role,
    };

    return {
      success: true,
      access_token: this.jwtService.sign(payload),
      user: {
        id: user.id,
        email: user.email,
        name: user.name,
        role: user.role,
        isActive: user.isActive,
        lastLoginAt: user.lastLoginAt,
        createdAt: user.createdAt
      },
    };
  }

  // Register user - SIMPLE VERSION
  async register(registerDto: { name: string; email: string; password: string }) {
    try {
      // Create user directly
      const user = await this.usersService.createSimpleUser(registerDto);

      // Remove password from response
      const { password, ...userWithoutSensitive } = user;

      return {
        success: true,
        message: 'Registration successful! You can now log in.',
        user: userWithoutSensitive,
      };
    } catch (error) {
      console.error('Registration error:', error);
      
      if (error instanceof ConflictException) {
        throw error;
      }
      
      throw new InternalServerErrorException('Registration failed. Please try again.');
    }
  }

  // Simple activation (always success for now)
  async activateUser(token: string): Promise<{ success: boolean; message: string }> {
    return { 
      success: true, 
      message: 'Account activated successfully! You can now log in.' 
    };
  }

  // Health check
  async healthCheck() {
    return { 
      status: 'OK', 
      service: 'Auth Service',
      timestamp: new Date().toISOString() 
    };
  }
}