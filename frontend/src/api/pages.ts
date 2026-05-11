import apiClient from './client';
import type { Page, PageCreateRequest, PageUpdateRequest } from '@/types';

export const pagesAPI = {
  async list(siteId: string): Promise<Page[]> {
    const response = await apiClient.get<Page[]>(`/sites/${siteId}/pages`);
    return response.data;
  },

  async create(siteId: string, data: PageCreateRequest): Promise<Page> {
    const response = await apiClient.post<Page>(`/sites/${siteId}/pages`, data);
    return response.data;
  },

  async get(siteId: string, pageId: string): Promise<Page> {
    const response = await apiClient.get<Page>(`/sites/${siteId}/pages/${pageId}`);
    return response.data;
  },

  async update(siteId: string, pageId: string, data: PageUpdateRequest): Promise<Page> {
    const response = await apiClient.put<Page>(`/sites/${siteId}/pages/${pageId}`, data);
    return response.data;
  },

  async updateContent(siteId: string, pageId: string, data: Partial<PageUpdateRequest>): Promise<Page> {
    const response = await apiClient.put<Page>(`/sites/${siteId}/pages/${pageId}/content`, data);
    return response.data;
  },

  async delete(siteId: string, pageId: string): Promise<void> {
    await apiClient.delete(`/sites/${siteId}/pages/${pageId}`);
  },

  async reorder(siteId: string, pageIds: string[]): Promise<void> {
    await apiClient.put(`/sites/${siteId}/pages/reorder`, { page_ids: pageIds });
  },
};
