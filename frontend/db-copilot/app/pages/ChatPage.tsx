"use client";
import { useState, useRef, useEffect } from "react";

interface Props {
  connectionId: string;
  onDisconnect: () => void;
}

interface Message {
  id: string;
  text: string;
  isUser: boolean;
  timestamp: Date;
  isTyping?: boolean;
}

export const ChatPage = ({ connectionId, onDisconnect }: Props) => {
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "welcome",
      text: "👋 Welcome to Database Copilot! I'm here to help you with your database queries. Ask me anything about your database structure, data, or operations.",
      isUser: false,
      timestamp: new Date()
    }
  ]);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSend = async () => {
    if (!message.trim() || isLoading) return;
    
    const userMessage: Message = {
      id: Date.now().toString(),
      text: message,
      isUser: true,
      timestamp: new Date()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setMessage("");
    setIsLoading(true);

    // Simulate AI typing
    setTimeout(() => {
      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: "I understand your query. Let me analyze your database and provide you with the information you need. This is a placeholder response - the actual AI integration will be implemented next.",
        isUser: false,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, aiMessage]);
      setIsLoading(false);
    }, 1500);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Header */}
      <div className="bg-black/20 backdrop-blur-sm border-b border-white/10">
        <div className="max-w-6xl mx-auto px-6 py-4 flex justify-between items-center">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center">
              <svg className="w-6 h-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
            </div>
            <div>
              <h1 className="text-xl font-bold text-white">Database Copilot</h1>
              <p className="text-sm text-slate-300">Connected • ID: {connectionId.slice(0, 8)}...</p>
            </div>
          </div>
          <button 
            onClick={onDisconnect}
            className="flex items-center space-x-2 px-4 py-2 bg-red-500/20 border border-red-500/30 text-red-300 rounded-lg hover:bg-red-500/30 transition-all duration-200"
          >
            <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
            </svg>
            <span>Disconnect</span>
          </button>
        </div>
      </div>

      {/* Chat Container */}
      <div className="max-w-6xl mx-auto p-6 h-[calc(100vh-88px)] flex flex-col">
        {/* Messages Area */}
        <div className="flex-1 bg-white/5 backdrop-blur-lg rounded-2xl border border-white/10 p-6 mb-6 overflow-hidden flex flex-col">
          <div className="flex-1 overflow-y-auto space-y-6 pr-2">
            {messages.map((msg) => (
              <div key={msg.id} className={`flex ${msg.isUser ? 'justify-end' : 'justify-start'} animate-in slide-in-from-bottom duration-300`}>
                <div className={`flex items-start space-x-3 max-w-2xl ${
                  msg.isUser ? 'flex-row-reverse space-x-reverse' : ''
                }`}>
                  {/* Avatar */}
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                    msg.isUser 
                      ? 'bg-gradient-to-r from-blue-500 to-blue-600' 
                      : 'bg-gradient-to-r from-purple-500 to-purple-600'
                  }`}>
                    {msg.isUser ? (
                      <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                      </svg>
                    ) : (
                      <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                      </svg>
                    )}
                  </div>
                  
                  {/* Message Bubble */}
                  <div className={`rounded-2xl px-4 py-3 shadow-lg ${
                    msg.isUser 
                      ? 'bg-gradient-to-r from-blue-600 to-blue-700 text-white' 
                      : 'bg-white/10 text-white border border-white/20'
                  }`}>
                    <p className="text-sm leading-relaxed">{msg.text}</p>
                    <p className={`text-xs mt-2 opacity-70 ${
                      msg.isUser ? 'text-blue-100' : 'text-slate-300'
                    }`}>
                      {msg.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                    </p>
                  </div>
                </div>
              </div>
            ))}
            
            {/* Typing Indicator */}
            {isLoading && (
              <div className="flex justify-start animate-in slide-in-from-bottom duration-300">
                <div className="flex items-start space-x-3 max-w-2xl">
                  <div className="w-8 h-8 rounded-full bg-gradient-to-r from-purple-500 to-purple-600 flex items-center justify-center">
                    <svg className="w-4 h-4 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                    </svg>
                  </div>
                  <div className="bg-white/10 border border-white/20 rounded-2xl px-4 py-3">
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-white/60 rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-white/60 rounded-full animate-bounce" style={{animationDelay: '0.1s'}}></div>
                      <div className="w-2 h-2 bg-white/60 rounded-full animate-bounce" style={{animationDelay: '0.2s'}}></div>
                    </div>
                  </div>
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Input Area */}
        <div className="bg-white/5 backdrop-blur-lg rounded-2xl border border-white/10 p-4">
          <div className="flex items-end space-x-4">
            <div className="flex-1">
              <textarea
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && !e.shiftKey && (e.preventDefault(), handleSend())}
                placeholder="Ask me about your database structure, queries, or data analysis..."
                className="w-full p-4 bg-white/5 border border-white/20 rounded-xl text-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all resize-none"
                rows={1}
                style={{ minHeight: '52px', maxHeight: '120px' }}
              />
            </div>
            <button 
              onClick={handleSend}
              disabled={!message.trim() || isLoading}
              className="p-4 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl hover:from-blue-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-105 transition-all duration-200 shadow-lg"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
            </button>
          </div>
          <div className="flex items-center justify-between mt-3 text-xs text-slate-400">
            <span>Press Enter to send, Shift+Enter for new line</span>
            <span>{message.length}/1000</span>
          </div>
        </div>
      </div>
    </div>
  );
};