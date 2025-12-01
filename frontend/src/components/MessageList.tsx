/**
 * Message list component with auto-scroll
 * WCAG 2.2 Level AA compliant
 */

import { useEffect, useRef } from 'react';
import { Message } from './Message';
import { FallbackBanner } from './FallbackBanner';
import type { ChatMessage } from '../types';

interface MessageListProps {
  messages: ChatMessage[];
  isLoading: boolean;
  showFallback: boolean;
  microsoftListUrl: string | null;
}

export function MessageList({
  messages,
  isLoading,
  showFallback,
  microsoftListUrl,
}: MessageListProps) {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  return (
    <div
      className="flex-1 overflow-y-auto px-4 py-6"
      role="log"
      aria-live="polite"
      aria-label="Chat conversation"
    >
      {messages.length === 0 && (
        <div className="text-center text-gray-500 mt-8">
          <h2 className="text-xl font-semibold mb-2">Welcome to HR Assistant!</h2>
          <p className="text-sm">
            Ask me anything about benefits, payroll, leave policies, and more.
          </p>
        </div>
      )}

      {messages.map((message, index) => (
        <Message key={index} message={message} />
      ))}

      {isLoading && (
        <div
          className="flex gap-3 mb-4"
          role="status"
          aria-label="Loading response"
        >
          <div className="flex-shrink-0 w-8 h-8 rounded-full bg-walmart-blue flex items-center justify-center">
            <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
          </div>
          <div className="bg-gray-100 rounded-lg px-4 py-3">
            <p className="text-sm text-gray-600">Thinking...</p>
          </div>
        </div>
      )}

      {showFallback && microsoftListUrl && (
        <FallbackBanner microsoftListUrl={microsoftListUrl} />
      )}

      <div ref={messagesEndRef} />
    </div>
  );
}
