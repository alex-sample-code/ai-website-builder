import { axiosInstance } from './client';
import type { FormDefinition, FormSubmission, FormSubmissionUpdateRequest, PaginatedResponse } from '@/types';

export const formsAPI = {
  async listDefinitions(siteId: string): Promise<FormDefinition[]> {
    const response = await axiosInstance.get<FormDefinition[]>(`/sites/${siteId}/forms`);
    return response.data;
  },

  async createDefinition(siteId: string, data: Partial<FormDefinition>): Promise<FormDefinition> {
    const response = await axiosInstance.post<FormDefinition>(`/sites/${siteId}/forms`, data);
    return response.data;
  },

  async updateDefinition(siteId: string, formId: string, data: Partial<FormDefinition>): Promise<FormDefinition> {
    const response = await axiosInstance.put<FormDefinition>(`/sites/${siteId}/forms/${formId}`, data);
    return response.data;
  },

  async listSubmissions(
    siteId: string,
    formId: string,
    params?: { page?: number; per_page?: number; status?: string }
  ): Promise<PaginatedResponse<FormSubmission>> {
    const response = await axiosInstance.get<PaginatedResponse<FormSubmission>>(
      `/sites/${siteId}/forms/${formId}/submissions`,
      { params }
    );
    return response.data;
  },

  async updateSubmissionStatus(
    siteId: string,
    submissionId: string,
    data: FormSubmissionUpdateRequest
  ): Promise<FormSubmission> {
    const response = await axiosInstance.put<FormSubmission>(
      `/sites/${siteId}/forms/submissions/${submissionId}/status`,
      data
    );
    return response.data;
  },

  async exportSubmissions(siteId: string, formId: string): Promise<Blob> {
    const response = await axiosInstance.get(`/sites/${siteId}/forms/${formId}/submissions/export`, {
      responseType: 'blob',
    });
    return response.data;
  },
};
