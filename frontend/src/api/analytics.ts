import { axiosInstance } from './client';
import type { AnalyticsOverview, PageAnalytics, SourceAnalytics, DeviceAnalytics } from '@/types';

export const analyticsAPI = {
  async getOverview(siteId: string, params?: { start_date?: string; end_date?: string }): Promise<AnalyticsOverview> {
    const response = await axiosInstance.get<AnalyticsOverview>(`/sites/${siteId}/analytics/overview`, { params });
    return response.data;
  },

  async getPageStats(siteId: string, params?: { start_date?: string; end_date?: string }): Promise<PageAnalytics[]> {
    const response = await axiosInstance.get<PageAnalytics[]>(`/sites/${siteId}/analytics/pages`, { params });
    return response.data;
  },

  async getSourceStats(siteId: string, params?: { start_date?: string; end_date?: string }): Promise<SourceAnalytics[]> {
    const response = await axiosInstance.get<SourceAnalytics[]>(`/sites/${siteId}/analytics/sources`, { params });
    return response.data;
  },

  async getDeviceStats(siteId: string, params?: { start_date?: string; end_date?: string }): Promise<DeviceAnalytics[]> {
    const response = await axiosInstance.get<DeviceAnalytics[]>(`/sites/${siteId}/analytics/devices`, { params });
    return response.data;
  },
};
