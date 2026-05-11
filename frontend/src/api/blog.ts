import apiClient from './client';
import type { BlogPost, BlogCategory, BlogTag, BlogPostCreateRequest, PaginatedResponse } from '@/types';

export const blogAPI = {
  async listPosts(siteId: string, params?: { page?: number; per_page?: number; status?: string }): Promise<PaginatedResponse<BlogPost>> {
    const response = await apiClient.get<PaginatedResponse<BlogPost>>(`/sites/${siteId}/blog/posts`, { params });
    return response.data;
  },

  async createPost(siteId: string, data: BlogPostCreateRequest): Promise<BlogPost> {
    const response = await apiClient.post<BlogPost>(`/sites/${siteId}/blog/posts`, data);
    return response.data;
  },

  async getPost(siteId: string, postId: string): Promise<BlogPost> {
    const response = await apiClient.get<BlogPost>(`/sites/${siteId}/blog/posts/${postId}`);
    return response.data;
  },

  async updatePost(siteId: string, postId: string, data: Partial<BlogPostCreateRequest>): Promise<BlogPost> {
    const response = await apiClient.put<BlogPost>(`/sites/${siteId}/blog/posts/${postId}`, data);
    return response.data;
  },

  async deletePost(siteId: string, postId: string): Promise<void> {
    await apiClient.delete(`/sites/${siteId}/blog/posts/${postId}`);
  },

  async listCategories(siteId: string): Promise<BlogCategory[]> {
    const response = await apiClient.get<BlogCategory[]>(`/sites/${siteId}/blog/categories`);
    return response.data;
  },

  async createCategory(siteId: string, data: { name: string; slug: string }): Promise<BlogCategory> {
    const response = await apiClient.post<BlogCategory>(`/sites/${siteId}/blog/categories`, data);
    return response.data;
  },

  async listTags(siteId: string): Promise<BlogTag[]> {
    const response = await apiClient.get<BlogTag[]>(`/sites/${siteId}/blog/tags`);
    return response.data;
  },
};
