/**
 * Individual chat message component
 * WCAG 2.2 Level AA compliant
 */

import { Bot, User } from 'lucide-react';
import type { ChatMessage } from '../types';

interface MessageProps {
  message: ChatMessage;
}

export function Message({ message }: MessageProps) {
  const isUser = message.role === 'user';
  const timestamp = message.timestamp || new Date();

  return (
    <div
      className={`flex gap-3 mb-4 ${isUser ? 'justify-end' : 'justify-start'}`}
      role="article"
      aria-label={`${isUser ? 'Your' : 'Assistant'} message`}
    >
      {!isUser && (
        <div
          className="flex-shrink-0 w-8 h-8 rounded-full bg-walmart-blue flex items-center justify-center"
          aria-hidden="true"
        >
          <Bot className="w-5 h-5 text-white" />
        </div>
      )}

      <div
        className={`max-w-[70%] rounded-lg px-4 py-3 ${
          isUser
            ? 'bg-walmart-blue text-white'
            : 'bg-gray-100 text-gray-900'
        }`}
      >
        <p className="text-sm md:text-base whitespace-pre-wrap break-words">
          {message.content}
        </p>
        <time
          className={`text-xs mt-1 block ${
            isUser ? 'text-blue-100' : 'text-gray-500'
          }`}
          dateTime={timestamp.toISOString()}
        >
          {timestamp.toLocaleTimeString([], {
            hour: '2-digit',
            minute: '2-digit',
          })}
        </time>
      </div>

      {isUser && (
        <div
          className="flex-shrink-0 w-8 h-8 rounded-full bg-gray-300 flex items-center justify-center"
          aria-hidden="true"
        >
          <User className="w-5 h-5 text-gray-700" />
        </div>
      )}
    </div>
  );
}
