import 'reflect-metadata'; // ADD THIS AT THE VERY TOP
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

// Debug: Check environment variables
console.log('Database Configuration:', {
  DB_HOST: process.env.DB_HOST,
  DB_PORT: process.env.DB_PORT,
  DB_USERNAME: process.env.DB_USERNAME,
  DB_NAME: process.env.DB_NAME,
  DB_PASSWORD: process.env.DB_PASSWORD ? '***' : 'MISSING',
  NODE_ENV: process.env.NODE_ENV
});

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  
  // Enable CORS for both HTTP and WebSocket connections
  app.enableCors({
    origin: ['http://localhost:5173', 'http://localhost:3000'],
    credentials: true,
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization', 'X-Requested-With'],
  });
  
  await app.listen(3001);
  console.log('Application is running on: http://localhost:3001');
}
bootstrap();