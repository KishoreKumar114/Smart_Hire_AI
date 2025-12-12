import { Controller, Get } from '@nestjs/common';

@Controller()
export class AppController {
  @Get('hello')  // ← this creates /hello route
  getHello() {
    return { message: 'Hello from NestJS!' };
  }
}
