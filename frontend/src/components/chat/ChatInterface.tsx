'use client';

import React, { useState } from 'react';
import { MessageSquare, Play, Send, Bot, User } from 'lucide-react';
import { cn } from '@/lib/utils';
import { useWorkbenchStore } from '@/store/workbench';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  id: string;
}

export const ChatInterface = () => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState<Message[]>([
    { 
      role: 'assistant', 
      content: 'Hello! I am MasterBlack AI. I can help you build applications, run commands, and debug code. What should we work on?',
      id: '1'
    }
  ]);
  const { isThinking, setIsThinking } = useWorkbenchStore();

  const handleSend = () => {
    if (!input.trim() || isThinking) return;

    const userMessage: Message = {
      role: 'user',
      content: input,
      id: Date.now().toString()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsThinking(true);

    // Mock response for now
    setTimeout(() => {
      const assistantMessage: Message = {
        role: 'assistant',
        content: `I'll help you with "${input}". I'm starting the reasoning process...`,
        id: (Date.now() + 1).toString()
      };
      setMessages(prev => [...prev, assistantMessage]);
      setIsThinking(false);
    }, 1500);
  };

  return (
    <div className="w-80 flex flex-col h-full bg-[#252526] border-l border-[#333]">
      <div className="p-4 border-b border-[#333] flex items-center justify-between text-gray-300">
        <div className="flex items-center gap-2 font-semibold">
          <MessageSquare size={16} /> AI Chat
        </div>
        {isThinking && (
          <div className="flex items-center gap-1">
            <div className="w-1.5 h-1.5 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
            <div className="w-1.5 h-1.5 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
            <div className="w-1.5 h-1.5 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
          </div>
        )}
      </div>
      
      <div className="flex-1 p-4 overflow-y-auto space-y-4">
        {messages.map((msg) => (
          <div 
            key={msg.id} 
            className={cn(
              "flex gap-3",
              msg.role === 'user' ? "flex-row-reverse" : ""
            )}
          >
            <div className={cn(
              "w-8 h-8 rounded-full flex items-center justify-center shrink-0",
              msg.role === 'assistant' ? "bg-blue-600 text-white" : "bg-[#3c3c3c] text-gray-300"
            )}>
              {msg.role === 'assistant' ? <Bot size={18} /> : <User size={18} />}
            </div>
            <div className={cn(
              "max-w-[85%] p-3 rounded-lg text-sm",
              msg.role === 'assistant' ? "bg-[#2d2d2d] text-gray-200" : "bg-blue-700 text-white"
            )}>
              {msg.content}
            </div>
          </div>
        ))}
      </div>
      
      <div className="p-4 border-t border-[#333]">
        <div className="relative">
          <textarea 
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSend();
              }
            }}
            placeholder="Ask anything..."
            className="w-full bg-[#3c3c3c] text-gray-200 text-sm rounded-md p-3 pr-10 focus:outline-none focus:ring-1 focus:ring-blue-500 min-h-[100px] max-h-[300px] resize-none"
          />
          <button 
            onClick={handleSend}
            disabled={!input.trim() || isThinking}
            className="absolute bottom-3 right-3 p-1.5 bg-blue-600 rounded-md hover:bg-blue-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <Send size={14} className="text-white fill-current" />
          </button>
        </div>
      </div>
    </div>
  );
};
