import { Entity, PrimaryGeneratedColumn, Column, CreateDateColumn, ManyToOne, JoinColumn } from 'typeorm';
import { User } from '../users/user.entity';

@Entity('messages')
export class Message {
  @PrimaryGeneratedColumn()
  id!: number;

  @Column('text')
  content: string;

  @ManyToOne(() => User, { eager: true })
  @JoinColumn({ name: 'senderId' })
  sender: User;

  @ManyToOne(() => User, { eager: true })
  @JoinColumn({ name: 'receiverId' })
  receiver: User;

  @Column()
  senderId: number;

  @Column()
  receiverId: number;

  @Column({ default: false })
  isSeen: boolean; // NEW: Seen status

  @CreateDateColumn()
  createdAt: Date;

  @Column({ nullable: true })
  seenAt: Date;
}