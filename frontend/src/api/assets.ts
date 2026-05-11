import apiClient, { axiosInstance } from './client';
import type { Asset, AssetUploadResponse } from '@/types';

export const assetsAPI = {
  async list(siteId: string, params?: { folder?: string }): Promise<Asset[]> {
    const response = await apiClient.get<Asset[]>(`/sites/${siteId}/assets`, { params });
    return response.data;
  },

  async upload(siteId: string, file: File, folder?: string): Promise<AssetUploadResponse> {
    const formData = new FormData();
    formData.append('file', file);
    if (folder) {
      formData.append('folder', folder);
    }

    const response = await axiosInstance.post<AssetUploadResponse>(
      `/sites/${siteId}/assets/upload`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );

    return response.data;
  },

  async delete(siteId: string, assetId: string): Promise<void> {
    await apiClient.delete(`/sites/${siteId}/assets/${assetId}`);
  },
};
