/**
 * Chat input component with form handling
 * WCAG 2.2 Level AA compliant with keyboard navigation
 */

import { useState, FormEvent } from 'react';
import { Send } from 'lucide-react';

interface ChatInputProps {
  onSendMessage: (message: string) => void;
  disabled: boolean;
}

export function ChatInput({ onSendMessage, disabled }: ChatInputProps) {
  const [input, setInput] = useState('');

  const handleSubmit = (e: FormEvent) => {
    e.preventDefault();
    if (input.trim() && !disabled) {
      onSendMessage(input.trim());
      setInput('');
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    // Send on Enter, new line on Shift+Enter
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="border-t border-gray-200 bg-white p-4"
    >
      <div className="flex gap-2 max-w-4xl mx-auto">
        <label htmlFor="chat-input" className="sr-only">
          Type your HR question
        </label>
        <input
          id="chat-input"
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={disabled}
          placeholder="Ask me about benefits, PTO, payroll, or other HR topics..."
          className="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-walmart-blue focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed text-gray-900 placeholder-gray-500"
          aria-label="Chat message input"
          autoComplete="off"
        />
        <button
          type="submit"
          disabled={disabled || !input.trim()}
          className="px-6 py-3 bg-walmart-blue text-white rounded-lg hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-walmart-blue focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2 font-medium"
          aria-label="Send message"
        >
          <span className="hidden sm:inline">Send</span>
          <Send className="w-5 h-5" aria-hidden="true" />
        </button>
      </div>
      <p className="text-xs text-gray-500 mt-2 max-w-4xl mx-auto">
        Press Enter to send, Shift+Enter for new line
      </p>
    </form>
  );
}
