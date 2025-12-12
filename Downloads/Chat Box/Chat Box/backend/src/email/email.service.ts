import { Injectable } from '@nestjs/common';
import * as nodemailer from 'nodemailer';

@Injectable()
export class EmailService {
  private transporter;

  constructor() {
    this.initializeEmail();
  }

  private initializeEmail() {
    // Log configuration for debugging
    console.log('📧 Email Service Configuration:', {
      host: process.env.SMTP_HOST,
      port: process.env.SMTP_PORT,
      user: process.env.SMTP_USER ? 'SET' : 'MISSING',
      pass: process.env.SMTP_PASS ? 'SET' : 'MISSING',
      frontendUrl: process.env.FRONTEND_URL
    });

    if (!process.env.SMTP_USER || !process.env.SMTP_PASS) {
      console.error('❌ SMTP credentials missing! Emails will not be sent.');
      return;
    }

    this.transporter = nodemailer.createTransport({
      host: process.env.SMTP_HOST || 'smtp.gmail.com',
      port: parseInt(process.env.SMTP_PORT || '587'),
      secure: false, // Use false for TLS
      auth: {
        user: process.env.SMTP_USER,
        pass: process.env.SMTP_PASS,
      },
    });

    // Test connection on startup
    this.testConnection();
  }

  private async testConnection() {
    if (!this.transporter) {
      console.log('❌ Email transporter not created - check SMTP credentials');
      return;
    }

    try {
      await this.transporter.verify();
      console.log('✅ SMTP Connection verified - ready to send emails');
    } catch (error) {
      console.error('❌ SMTP Connection failed:', error.message);
    }
  }

  async sendActivationEmail(email: string, token: string, name: string): Promise<boolean> {
    // Check if transporter is available
    if (!this.transporter) {
      console.error('❌ Email transporter not available - check SMTP configuration');
      return false;
    }

    const frontendUrl = process.env.FRONTEND_URL || 'http://localhost:3000';
    const activationLink = `${frontendUrl}/activate/${token}`;
    
    console.log(`📨 Attempting to send activation email to: ${email}`);
    console.log(`🔗 Activation link: ${activationLink}`);

    const mailOptions = {
      from: process.env.EMAIL_FROM || 'noreply@yourapp.com',
      to: email,
      subject: 'Activate Your ChatApp Account',
      html: `
        <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
          <h1 style="color: #333; text-align: center;">Welcome to ChatApp, ${name}!</h1>
          <p style="font-size: 16px;">Thank you for registering. Please activate your account:</p>
          
          <div style="text-align: center; margin: 30px 0;">
            <a href="${activationLink}" 
               style="background-color: #3b82f6; color: white; padding: 14px 28px; text-decoration: none; border-radius: 6px; display: inline-block; font-weight: bold;">
              Activate Account
            </a>
          </div>
          
          <p>Or copy this link in your browser:</p>
          <p style="word-break: break-all; color: #3b82f6; background: #f0f4ff; padding: 10px; border-radius: 4px;">
            ${activationLink}
          </p>
        </div>
      `,
    };

    try {
      const info = await this.transporter.sendMail(mailOptions);
      console.log(`✅ Activation email sent successfully to: ${email}`);
      console.log(`📫 Message ID: ${info.messageId}`);
      return true;
    } catch (error) {
      console.error('❌ Failed to send activation email:', error);
      console.error('Error details:', {
        code: error.code,
        command: error.command,
        response: error.response
      });
      return false;
    }
  }
}