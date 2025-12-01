/**
 * API service for communicating with the backend
 */

import type { ChatRequest, ChatResponse, AppConfig } from './types';

const API_BASE_URL = import.meta.env.VITE_API_URL || '';

/**
 * Send a chat message to the backend
 */
export async function sendChatMessage(
  request: ChatRequest
): Promise<ChatResponse> {
  const response = await fetch(`${API_BASE_URL}/api/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
}

/**
 * Get app configuration from backend
 */
export async function getConfig(): Promise<AppConfig> {
  const response = await fetch(`${API_BASE_URL}/api/config`);

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
}
