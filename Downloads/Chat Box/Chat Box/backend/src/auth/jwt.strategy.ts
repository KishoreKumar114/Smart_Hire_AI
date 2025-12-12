import { ExtractJwt, Strategy } from 'passport-jwt';
import { PassportStrategy } from '@nestjs/passport';
import { Injectable, UnauthorizedException } from '@nestjs/common';
import { UsersService } from '../users/users.service';

@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  constructor(private usersService: UsersService) {
    super({
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      ignoreExpiration: false,
      secretOrKey: process.env.JWT_SECRET || 'your-secret-key',
    });
  }

  async validate(payload: any) {
    console.log('🔐 JWT Strategy - Validating payload for user ID:', payload.sub);
    
    try {
      // Use findById method (not findOne)
      const user = await this.usersService.findById(payload.sub);
      
      if (!user) {
        console.error('❌ JWT Strategy - User not found in database for id:', payload.sub);
        throw new UnauthorizedException('User not found');
      }

      // TEMPORARY: Skip activation check to match your flow
      // if (!user.isActive) {
      //   console.error('❌ JWT Strategy - User account not activated:', payload.sub);
      //   throw new UnauthorizedException('Account not activated');
      // }

      console.log('✅ JWT Strategy - User validated successfully:', {
        id: user.id,
        email: user.email,
        name: user.name,
        role: user.role
      });
      
      return {
        id: user.id,
        email: user.email,
        name: user.name,
        role: user.role,
        isActive: user.isActive,
        lastLoginAt: user.lastLoginAt,
        createdAt: user.createdAt,
      };
    } catch (error) {
      console.error('❌ JWT Strategy - Error validating user:', error);
      throw new UnauthorizedException('Invalid token');
    }
  }
}