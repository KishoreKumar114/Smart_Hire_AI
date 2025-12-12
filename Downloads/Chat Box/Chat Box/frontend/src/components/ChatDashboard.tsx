import React, { useState, useEffect, useRef } from 'react';
import { usersApi, messagesApi } from '../service/api';
import { webSocketService } from '../service/websocket.service';
import type { User, Message, ChatContact } from '../types';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

const ChatDashboard: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const [contacts, setContacts] = useState<ChatContact[]>([]);
  const [selectedContact, setSelectedContact] = useState<User | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [newMessage, setNewMessage] = useState('');
  const [loading, setLoading] = useState(true);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Load contacts and setup WebSocket
  useEffect(() => {
    if (user) {
      loadContacts();
      setupWebSocketListeners();
    }

    return () => {
      // Cleanup WebSocket listeners
      webSocketService.off('newMessage', handleNewMessage);
      webSocketService.off('userOnline', handleUserOnline);
      webSocketService.off('userOffline', handleUserOffline);
      webSocketService.off('messagesSeen', handleMessagesSeen);
    };
  }, [user]);

  // Load messages when contact is selected
  useEffect(() => {
    if (selectedContact) {
      loadMessages(selectedContact.id);
      markMessagesAsSeen(selectedContact.id);
    }
  }, [selectedContact]);

  // Scroll to bottom when messages change
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const loadContacts = async () => {
    try {
      setLoading(true);
      const [usersResponse, unreadResponse] = await Promise.all([
        usersApi.getAllUsersExceptMe(),
        messagesApi.getUnreadCounts()
      ]);

      const users: User[] = usersResponse.data;
      const unreadCounts: { [key: number]: number } = unreadResponse.data;

      const contactsList: ChatContact[] = users.map(contactUser => ({
        user: contactUser,
        unreadCount: unreadCounts[contactUser.id] || 0
      }));

      setContacts(contactsList);
    } catch (error) {
      console.error('Error loading contacts:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadMessages = async (contactId: number) => {
    try {
      const response = await messagesApi.getConversation(contactId);
      setMessages(response.data);
    } catch (error) {
      console.error('Error loading messages:', error);
    }
  };

  const markMessagesAsSeen = async (senderId: number) => {
    try {
      await messagesApi.markMessagesAsSeen(senderId);
      // Update local state
      setContacts(prev => prev.map(contact => 
        contact.user.id === senderId 
          ? { ...contact, unreadCount: 0 }
          : contact
      ));
      
      // Notify via WebSocket
      webSocketService.emit('markMessagesSeen', { senderId });
    } catch (error) {
      console.error('Error marking messages as seen:', error);
    }
  };

  const setupWebSocketListeners = () => {
    webSocketService.on('newMessage', handleNewMessage);
    webSocketService.on('userOnline', handleUserOnline);
    webSocketService.on('userOffline', handleUserOffline);
    webSocketService.on('messagesSeen', handleMessagesSeen);
  };

  const handleNewMessage = (message: Message) => {
    // If message is for current conversation, add to messages
    if (selectedContact && 
        (message.senderId === selectedContact.id || message.receiverId === selectedContact.id)) {
      setMessages(prev => [...prev, message]);
    }

    // Update contacts with new message and increment unread count
    setContacts(prev => prev.map(contact => {
      if (contact.user.id === message.senderId) {
        const shouldIncrementUnread = contact.user.id !== selectedContact?.id;
        return {
          ...contact,
          unreadCount: shouldIncrementUnread ? contact.unreadCount + 1 : 0
        };
      }
      return contact;
    }));
  };

  const handleUserOnline = (data: { userId: number }) => {
    setContacts(prev => prev.map(contact =>
      contact.user.id === data.userId
        ? { ...contact, user: { ...contact.user, isOnline: true } }
        : contact
    ));
  };

  const handleUserOffline = (data: { userId: number }) => {
    setContacts(prev => prev.map(contact =>
      contact.user.id === data.userId
        ? { ...contact, user: { ...contact.user, isOnline: false } }
        : contact
    ));
  };

  const handleMessagesSeen = (data: { receiverId: number }) => {
    // Update messages as seen in current conversation
    if (selectedContact && data.receiverId === user?.id) {
      setMessages(prev => prev.map(msg =>
        msg.senderId === user.id ? { ...msg, isSeen: true } : msg
      ));
    }
  };

  const sendMessage = () => {
    if (!newMessage.trim() || !selectedContact || !user) return;

    const messageData = {
      receiverId: selectedContact.id,
      content: newMessage.trim()
    };

    webSocketService.emit('sendMessage', messageData);
    
    // Optimistically add message to UI
    const optimisticMessage: Message = {
      id: Date.now(), // Temporary ID
      content: newMessage.trim(),
      sender: user,
      receiver: selectedContact,
      senderId: user.id, // This is now number
      receiverId: selectedContact.id, // This is now number
      isSeen: false,
      createdAt: new Date().toISOString()
    };
    
    setMessages(prev => [...prev, optimisticMessage]);
    setNewMessage('');
  };

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleLogout = () => {
    logout();
    webSocketService.disconnect();
    navigate('/login');
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading contacts...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar - Contacts List */}
      <div className="w-1/3 bg-white border-r border-gray-200 flex flex-col">
        <div className="p-4 border-b border-gray-200">
          <div className="flex justify-between items-center">
            <h1 className="text-xl font-bold text-gray-800">Chat App</h1>
            <div className="flex items-center space-x-3">
              <span className="text-sm text-gray-600">Hi, {user?.name}</span>
              <button
                onClick={handleLogout}
                className="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded text-sm transition-colors"
              >
                Logout
              </button>
            </div>
          </div>
        </div>

        <div className="p-4 flex-1 overflow-y-auto">
          <h2 className="text-lg font-semibold text-gray-700 mb-4">Contacts</h2>
          <div className="space-y-2">
            {contacts.map(contact => (
              <div
                key={contact.user.id}
                onClick={() => setSelectedContact(contact.user)}
                className={`p-3 rounded-lg cursor-pointer transition-all duration-200 ${
                  selectedContact?.id === contact.user.id
                    ? 'bg-blue-100 border-l-4 border-blue-500 shadow-sm'
                    : 'bg-gray-50 hover:bg-gray-100 border-l-4 border-transparent'
                }`}
              >
                <div className="flex justify-between items-center">
                  <div className="flex items-center space-x-3">
                    <div className="relative">
                      <div className="w-10 h-10 bg-blue-500 rounded-full flex items-center justify-center text-white font-semibold text-sm">
                        {contact.user.name.charAt(0).toUpperCase()}
                      </div>
                      <div
                        className={`absolute bottom-0 right-0 w-3 h-3 rounded-full border-2 border-white ${
                          contact.user.isOnline ? 'bg-green-500' : 'bg-gray-400'
                        }`}
                        title={contact.user.isOnline ? 'Online' : 'Offline'}
                      />
                    </div>
                    <div>
                      <div className="font-semibold text-gray-800">{contact.user.name}</div>
                      <div className="text-xs text-gray-500">
                        {contact.user.isOnline ? 'Online' : 'Last seen recently'}
                      </div>
                    </div>
                  </div>
                  {contact.unreadCount > 0 && (
                    <span className="bg-red-500 text-white text-xs rounded-full px-2 py-1 min-w-5 text-center font-semibold">
                      {contact.unreadCount}
                    </span>
                  )}
                </div>
              </div>
            ))}
            {contacts.length === 0 && (
              <div className="text-center text-gray-500 py-8">
                <p>No other users found</p>
                <p className="text-sm">Other users will appear here when they register</p>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Chat Area */}
      <div className="flex-1 flex flex-col">
        {selectedContact ? (
          <>
            {/* Chat Header */}
            <div className="bg-white border-b border-gray-200 p-4">
              <div className="flex items-center space-x-3">
                <div className="relative">
                  <div className="w-10 h-10 bg-green-500 rounded-full flex items-center justify-center text-white font-semibold text-sm">
                    {selectedContact.name.charAt(0).toUpperCase()}
                  </div>
                  <div
                    className={`absolute bottom-0 right-0 w-3 h-3 rounded-full border-2 border-white ${
                      selectedContact.isOnline ? 'bg-green-500' : 'bg-gray-400'
                    }`}
                  />
                </div>
                <div>
                  <div className="font-semibold text-gray-800">{selectedContact.name}</div>
                  <div className="text-sm text-gray-500">
                    {selectedContact.isOnline ? 'Online' : 'Offline'}
                  </div>
                </div>
              </div>
            </div>

            {/* Messages Area */}
            <div className="flex-1 overflow-y-auto p-4 bg-gray-50">
              <div className="space-y-4">
                {messages.map(message => (
                  <div
                    key={message.id}
                    className={`flex ${
                      message.senderId === user?.id ? 'justify-end' : 'justify-start'
                    }`}
                  >
                    <div
                      className={`max-w-xs lg:max-w-md px-4 py-2 rounded-2xl ${
                        message.senderId === user?.id
                          ? 'bg-blue-500 text-white rounded-br-none'
                          : 'bg-white text-gray-800 rounded-bl-none shadow-sm'
                      }`}
                    >
                      <div className="text-sm">{message.content}</div>
                      <div
                        className={`text-xs mt-1 flex justify-between items-center ${
                          message.senderId === user?.id ? 'text-blue-100' : 'text-gray-500'
                        }`}
                      >
                        <span>{new Date(message.createdAt).toLocaleTimeString([], { 
                          hour: '2-digit', 
                          minute: '2-digit' 
                        })}</span>
                        {message.senderId === user?.id && (
                          <span className="ml-2">
                            {message.isSeen ? '✓✓' : '✓'}
                          </span>
                        )}
                      </div>
                    </div>
                  </div>
                ))}
                <div ref={messagesEndRef} />
              </div>
            </div>

            {/* Message Input */}
            <div className="bg-white border-t border-gray-200 p-4">
              <div className="flex space-x-3">
                <input
                  type="text"
                  value={newMessage}
                  onChange={(e) => setNewMessage(e.target.value)}
                  onKeyPress={handleKeyPress}
                  placeholder="Type a message..."
                  className="flex-1 border border-gray-300 rounded-full px-4 py-3 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
                <button
                  onClick={sendMessage}
                  disabled={!newMessage.trim()}
                  className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-3 rounded-full transition-colors disabled:bg-blue-300 disabled:cursor-not-allowed flex items-center space-x-2"
                >
                  <span>Send</span>
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                  </svg>
                </button>
              </div>
            </div>
          </>
        ) : (
          // No contact selected
          <div className="flex-1 flex items-center justify-center bg-gray-50">
            <div className="text-center text-gray-500">
              <div className="text-6xl mb-4">💬</div>
              <h2 className="text-2xl font-semibold mb-2">Welcome to Chat App</h2>
              <p className="text-lg">Select a contact to start chatting</p>
              <p className="text-sm mt-2">You'll see other users here when they register and login</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default ChatDashboard;