/**
 * Main chat container component
 * Manages chat state and API communication
 */

import { useState } from 'react';
import { Header } from './Header';
import { MessageList } from './MessageList';
import { ChatInput } from './ChatInput';
import { sendChatMessage } from '../api';
import type { ChatMessage } from '../types';

export function ChatContainer() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showFallback, setShowFallback] = useState(false);
  const [microsoftListUrl, setMicrosoftListUrl] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSendMessage = async (content: string) => {
    // Add user message
    const userMessage: ChatMessage = {
      role: 'user',
      content,
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);
    setShowFallback(false);
    setError(null);

    try {
      const response = await sendChatMessage({
        message: content,
        conversation_history: messages,
      });

      // Add assistant response
      const assistantMessage: ChatMessage = {
        role: 'assistant',
        content: response.response,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, assistantMessage]);
      setShowFallback(response.show_fallback);
      setMicrosoftListUrl(response.microsoft_list_url);
    } catch (err) {
      setError('Failed to get response. Please try again.');
      console.error('Chat error:', err);

      // Add error message
      const errorMessage: ChatMessage = {
        role: 'assistant',
        content:
          'Sorry, I encountered an error processing your request. Please try again or contact HR directly.',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      <Header />

      {error && (
        <div
          className="bg-red-50 border-l-4 border-red-500 p-4 mx-4 mt-4 rounded-r-lg"
          role="alert"
        >
          <p className="text-sm text-red-800">{error}</p>
        </div>
      )}

      <MessageList
        messages={messages}
        isLoading={isLoading}
        showFallback={showFallback}
        microsoftListUrl={microsoftListUrl}
      />

      <ChatInput onSendMessage={handleSendMessage} disabled={isLoading} />
    </div>
  );
}
