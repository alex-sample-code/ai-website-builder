import { axiosInstance } from './client';
import type { Template } from '@/types';

export const templatesAPI = {
  async list(params?: { category?: string; is_premium?: boolean }): Promise<Template[]> {
    const response = await axiosInstance.get<Template[]>('/templates', { params });
    return response.data;
  },

  async getPreview(templateId: string): Promise<{ preview_html: string; preview_url: string }> {
    const response = await axiosInstance.get<{ preview_html: string; preview_url: string }>(
      `/templates/${templateId}/preview`
    );
    return response.data;
  },
};
