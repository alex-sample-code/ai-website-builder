import axios, { AxiosInstance, InternalAxiosRequestConfig } from 'axios';
import type { APIResponse } from '@/types';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1';

class APIClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 30000,
    });

    this.setupInterceptors();
  }

  private setupInterceptors() {
    // Request interceptor - attach JWT token
    this.client.interceptors.request.use(
      (config: InternalAxiosRequestConfig) => {
        const token = localStorage.getItem('access_token');
        if (token && config.headers) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Response interceptor - handle 401 and errors
    this.client.interceptors.response.use(
      (response) => {
        return response;
      },
      async (error) => {
        const originalRequest = error.config;

        // Handle 401 - token expired
        if (error.response?.status === 401 && !originalRequest._retry) {
          originalRequest._retry = true;

          try {
            const refreshToken = localStorage.getItem('refresh_token');
            if (!refreshToken) {
              this.handleLogout();
              return Promise.reject(error);
            }

            // Try to refresh token
            const response = await axios.post(`${API_BASE_URL}/auth/refresh`, {
              refresh_token: refreshToken,
            });

            const { access_token } = response.data;
            localStorage.setItem('access_token', access_token);

            // Retry original request
            originalRequest.headers.Authorization = `Bearer ${access_token}`;
            return this.client(originalRequest);
          } catch (refreshError) {
            this.handleLogout();
            return Promise.reject(refreshError);
          }
        }

        return Promise.reject(error);
      }
    );
  }

  private handleLogout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    window.location.href = '/login';
  }

  public getClient(): AxiosInstance {
    return this.client;
  }

  // Helper methods for common HTTP verbs
  public async get<T>(url: string, config?: any): Promise<APIResponse<T>> {
    const response = await this.client.get<APIResponse<T>>(url, config);
    return response.data;
  }

  public async post<T>(url: string, data?: any, config?: any): Promise<APIResponse<T>> {
    const response = await this.client.post<APIResponse<T>>(url, data, config);
    return response.data;
  }

  public async put<T>(url: string, data?: any, config?: any): Promise<APIResponse<T>> {
    const response = await this.client.put<APIResponse<T>>(url, data, config);
    return response.data;
  }

  public async delete<T>(url: string, config?: any): Promise<APIResponse<T>> {
    const response = await this.client.delete<APIResponse<T>>(url, config);
    return response.data;
  }

  public async patch<T>(url: string, data?: any, config?: any): Promise<APIResponse<T>> {
    const response = await this.client.patch<APIResponse<T>>(url, data, config);
    return response.data;
  }
}

// Create singleton instance
const apiClient = new APIClient();

export default apiClient;
export const axiosInstance = apiClient.getClient();
