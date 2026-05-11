import apiClient, { axiosInstance } from './client';
import type { AISession, AISessionCreateRequest, AIMessageRequest, AIGenerateRequest } from '@/types';

export const aiAPI = {
  async createSession(data: AISessionCreateRequest): Promise<AISession> {
    const response = await apiClient.post<AISession>('/ai/sessions', data);
    return response.data;
  },

  async sendMessage(sessionId: string, data: AIMessageRequest): Promise<AISession> {
    const response = await apiClient.post<AISession>(`/ai/sessions/${sessionId}/message`, data);
    return response.data;
  },

  async uploadDocument(sessionId: string, file: File): Promise<{ message: string; s3_key: string }> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await axiosInstance.post<{ message: string; s3_key: string }>(
      `/ai/sessions/${sessionId}/upload`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );

    return response.data;
  },

  async generate(sessionId: string, data?: AIGenerateRequest): Promise<AISession> {
    const response = await apiClient.post<AISession>(`/ai/sessions/${sessionId}/generate`, data || {});
    return response.data;
  },

  async getStatus(sessionId: string): Promise<AISession> {
    const response = await apiClient.get<AISession>(`/ai/sessions/${sessionId}/status`);
    return response.data;
  },

  async regenerate(sessionId: string): Promise<AISession> {
    const response = await apiClient.post<AISession>(`/ai/sessions/${sessionId}/regenerate`, {});
    return response.data;
  },

  // SSE for streaming responses
  createEventSource(sessionId: string, message: string): EventSource {
    const token = localStorage.getItem('access_token');
    const url = `${import.meta.env.VITE_API_URL || '/api/v1'}/ai/sessions/${sessionId}/stream?message=${encodeURIComponent(message)}&token=${token}`;
    return new EventSource(url);
  },
};
