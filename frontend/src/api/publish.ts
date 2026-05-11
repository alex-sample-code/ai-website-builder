import { axiosInstance } from './client';
import type { SiteVersion, PublishRequest, DomainBindRequest, DomainStatus } from '@/types';

export const publishAPI = {
  async publish(siteId: string, data?: PublishRequest): Promise<SiteVersion> {
    const response = await axiosInstance.post<SiteVersion>(`/sites/${siteId}/publish`, data || {});
    return response.data;
  },

  async listVersions(siteId: string): Promise<SiteVersion[]> {
    const response = await axiosInstance.get<SiteVersion[]>(`/sites/${siteId}/versions`);
    return response.data;
  },

  async rollback(siteId: string, versionId: string): Promise<SiteVersion> {
    const response = await axiosInstance.post<SiteVersion>(`/sites/${siteId}/versions/${versionId}/rollback`, {});
    return response.data;
  },

  async getPreview(siteId: string): Promise<{ preview_url: string }> {
    const response = await axiosInstance.get<{ preview_url: string }>(`/sites/${siteId}/preview`);
    return response.data;
  },

  async bindDomain(siteId: string, data: DomainBindRequest): Promise<DomainStatus> {
    const response = await axiosInstance.post<DomainStatus>(`/sites/${siteId}/domain`, data);
    return response.data;
  },

  async getDomainStatus(siteId: string): Promise<DomainStatus> {
    const response = await axiosInstance.get<DomainStatus>(`/sites/${siteId}/domain`);
    return response.data;
  },

  async unbindDomain(siteId: string): Promise<void> {
    await axiosInstance.delete(`/sites/${siteId}/domain`);
  },

  async verifyDomain(siteId: string): Promise<DomainStatus> {
    const response = await axiosInstance.post<DomainStatus>(`/sites/${siteId}/domain/verify`, {});
    return response.data;
  },
};
