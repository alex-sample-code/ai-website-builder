import { axiosInstance } from './client';
import type { TeamMember, TeamInvitation, TeamInviteRequest, AuditLog, PaginatedResponse } from '@/types';

export const teamAPI = {
  async listMembers(): Promise<TeamMember[]> {
    const response = await axiosInstance.get<TeamMember[]>('/team/members');
    return response.data;
  },

  async invite(data: TeamInviteRequest): Promise<TeamInvitation> {
    const response = await axiosInstance.post<TeamInvitation>('/team/invite', data);
    return response.data;
  },

  async removeMember(memberId: string): Promise<void> {
    await axiosInstance.delete(`/team/members/${memberId}`);
  },

  async updateRole(memberId: string, role: 'owner' | 'editor' | 'viewer'): Promise<TeamMember> {
    const response = await axiosInstance.put<TeamMember>(`/team/members/${memberId}/role`, { role });
    return response.data;
  },

  async getAuditLogs(params?: { page?: number; per_page?: number }): Promise<PaginatedResponse<AuditLog>> {
    const response = await axiosInstance.get<PaginatedResponse<AuditLog>>('/team/audit-logs', { params });
    return response.data;
  },
};
