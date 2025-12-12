import { Controller, Post, Body, Get, Param, UseGuards, Req } from '@nestjs/common';
import { AuthService } from './auth.service';
import { JwtAuthGuard } from './jwt-auth.guard';

@Controller('auth')
export class AuthController {
  constructor(private authService: AuthService) {}

  // Register new user (no activation)
  @Post('register')
  async register(@Body() registerDto: { name: string; email: string; password: string }) {
    console.log('📝 Register request:', registerDto);
    return this.authService.register(registerDto);
  }

  // Login user
  @Post('login')
  async login(@Body() loginDto: { email: string; password: string }) {
    console.log('🔐 Login request for email:', loginDto.email);
    const user = await this.authService.validateUser(loginDto.email, loginDto.password);
    return this.authService.login(user);
  }

  // Simple activation (always success)
  @Get('activate/:token')
  async activate(@Param('token') token: string) {
    console.log('✅ Activation request for token:', token);
    return this.authService.activateUser(token);
  }

  // Get current user profile
  @Get('profile')
  @UseGuards(JwtAuthGuard)
  getProfile(@Req() req) {
    return req.user;
  }

  // Health check
  @Get('health')
  healthCheck() {
    console.log('🏥 Health check requested');
    return { 
      status: 'OK', 
      service: 'Auth Service',
      timestamp: new Date().toISOString(),
      endpoints: [
        'POST /auth/register',
        'POST /auth/login', 
        'GET  /auth/activate/:token',
        'GET  /auth/profile',
        'GET  /auth/health'
      ]
    };
  }
}