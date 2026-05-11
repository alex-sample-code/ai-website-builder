import apiClient from './client';
import type { Site, SiteCreateRequest } from '@/types';

export const sitesAPI = {
  async list(): Promise<Site[]> {
    const response = await apiClient.get<Site[]>('/sites');
    return response.data;
  },

  async create(data: SiteCreateRequest): Promise<Site> {
    const response = await apiClient.post<Site>('/sites', data);
    return response.data;
  },

  async get(siteId: string): Promise<Site> {
    const response = await apiClient.get<Site>(`/sites/${siteId}`);
    return response.data;
  },

  async update(siteId: string, data: Partial<Site>): Promise<Site> {
    const response = await apiClient.put<Site>(`/sites/${siteId}`, data);
    return response.data;
  },

  async delete(siteId: string): Promise<void> {
    await apiClient.delete(`/sites/${siteId}`);
  },
};
