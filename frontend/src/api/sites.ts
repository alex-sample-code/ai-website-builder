import { axiosInstance } from './client';
import type { Site, SiteCreateRequest } from '@/types';

export const sitesAPI = {
  async list(): Promise<Site[]> {
    const response = await axiosInstance.get<Site[]>('/sites');
    return response.data;
  },

  async create(data: SiteCreateRequest): Promise<Site> {
    const response = await axiosInstance.post<Site>('/sites', data);
    return response.data;
  },

  async get(siteId: string): Promise<Site> {
    const response = await axiosInstance.get<Site>(`/sites/${siteId}`);
    return response.data;
  },

  async update(siteId: string, data: Partial<Site>): Promise<Site> {
    const response = await axiosInstance.put<Site>(`/sites/${siteId}`, data);
    return response.data;
  },

  async delete(siteId: string): Promise<void> {
    await axiosInstance.delete(`/sites/${siteId}`);
  },
};
