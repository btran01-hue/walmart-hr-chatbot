/**
 * Type definitions for the HR Chatbot
 */

export interface ChatMessage {
  role: 'user' | 'assistant';
  content: string;
  timestamp?: Date;
}

export interface ChatRequest {
  message: string;
  conversation_history: ChatMessage[];
}

export interface ChatResponse {
  response: string;
  confidence: number;
  show_fallback: boolean;
  microsoft_list_url: string | null;
  sources: string[];
}

export interface AppConfig {
  microsoft_list_url: string;
  confidence_threshold: number;
}
