import { axiosInstance } from './client';
import type { SiteSettings, NavMenu } from '@/types';

export const settingsAPI = {
  async get(siteId: string): Promise<SiteSettings> {
    const response = await axiosInstance.get<SiteSettings>(`/sites/${siteId}/settings`);
    return response.data;
  },

  async update(siteId: string, data: Partial<SiteSettings>): Promise<SiteSettings> {
    const response = await axiosInstance.put<SiteSettings>(`/sites/${siteId}/settings`, data);
    return response.data;
  },

  async getNavMenus(siteId: string): Promise<NavMenu[]> {
    const response = await axiosInstance.get<NavMenu[]>(`/sites/${siteId}/nav-menus`);
    return response.data;
  },

  async updateNavMenus(siteId: string, data: Partial<NavMenu>[]): Promise<NavMenu[]> {
    const response = await axiosInstance.put<NavMenu[]>(`/sites/${siteId}/nav-menus`, data);
    return response.data;
  },
};
