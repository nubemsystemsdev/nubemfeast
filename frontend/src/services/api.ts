import axios, { AxiosInstance, AxiosError } from 'axios';
import type {
  Scan,
  ScanDetail,
  ScanCreate,
  ScanUpdate,
  ImageInfo,
  ImageUploadResponse,
  AnalysisResponse,
  Barrier,
  Guide,
  WheelchairProfile,
  WorldModel,
  PaginatedResponse,
  ScanStatus,
  BarrierSeverity,
  BarrierType,
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || '';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: `${API_BASE_URL}/api`,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    this.client.interceptors.response.use(
      (response) => response,
      (error: AxiosError) => {
        console.error('API Error:', error.response?.data || error.message);
        return Promise.reject(error);
      }
    );
  }

  // Scans
  async createScan(data: ScanCreate): Promise<Scan> {
    const response = await this.client.post<Scan>('/scans', data);
    return response.data;
  }

  async listScans(params?: {
    status?: ScanStatus;
    limit?: number;
    offset?: number;
  }): Promise<PaginatedResponse<Scan>> {
    const response = await this.client.get<PaginatedResponse<Scan>>('/scans', { params });
    return response.data;
  }

  async getScan(scanId: string): Promise<ScanDetail> {
    const response = await this.client.get<ScanDetail>(`/scans/${scanId}`);
    return response.data;
  }

  async updateScan(scanId: string, data: ScanUpdate): Promise<Scan> {
    const response = await this.client.patch<Scan>(`/scans/${scanId}`, data);
    return response.data;
  }

  async deleteScan(scanId: string): Promise<void> {
    await this.client.delete(`/scans/${scanId}`);
  }

  // Images
  async listImages(scanId: string): Promise<ImageInfo[]> {
    const response = await this.client.get<ImageInfo[]>(`/scans/${scanId}/images`);
    return response.data;
  }

  async uploadImages(scanId: string, files: File[]): Promise<ImageUploadResponse> {
    const formData = new FormData();
    files.forEach((file) => {
      formData.append('files', file);
    });

    const response = await this.client.post<ImageUploadResponse>(
      `/scans/${scanId}/images`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    return response.data;
  }

  async deleteImage(scanId: string, imageId: string): Promise<void> {
    await this.client.delete(`/scans/${scanId}/images/${imageId}`);
  }

  async reorderImages(scanId: string, imageIds: string[]): Promise<ImageInfo[]> {
    const response = await this.client.post<ImageInfo[]>(
      `/scans/${scanId}/images/reorder`,
      imageIds
    );
    return response.data;
  }

  getImageUrl(scanId: string, imageId: string): string {
    return `${API_BASE_URL}/api/scans/${scanId}/images/${imageId}/file`;
  }

  // Analysis
  async startAnalysis(
    scanId: string,
    options?: { wheelchair_profile_id?: string; force?: boolean }
  ): Promise<AnalysisResponse> {
    const response = await this.client.post<AnalysisResponse>(
      `/scans/${scanId}/analyze`,
      options
    );
    return response.data;
  }

  async getAnalysis(scanId: string): Promise<AnalysisResponse> {
    const response = await this.client.get<AnalysisResponse>(`/scans/${scanId}/analysis`);
    return response.data;
  }

  async listBarriers(
    scanId: string,
    params?: { severity?: BarrierSeverity; type?: BarrierType }
  ): Promise<Barrier[]> {
    const response = await this.client.get<Barrier[]>(
      `/scans/${scanId}/analysis/barriers`,
      { params }
    );
    return response.data;
  }

  async getImageBarriers(imageId: string): Promise<Barrier[]> {
    const response = await this.client.get<Barrier[]>(`/images/${imageId}/barriers`);
    return response.data;
  }

  // Navigation
  async getGuide(
    scanId: string,
    wheelchairProfileId?: string
  ): Promise<Guide> {
    const response = await this.client.get<Guide>(`/scans/${scanId}/guide`, {
      params: { wheelchair_profile_id: wheelchairProfileId },
    });
    return response.data;
  }

  async generateGuide(
    scanId: string,
    wheelchairProfileId?: string
  ): Promise<Guide> {
    const response = await this.client.post<Guide>(`/scans/${scanId}/guide`, {
      wheelchair_profile_id: wheelchairProfileId,
    });
    return response.data;
  }

  async getWorldModel(scanId: string): Promise<WorldModel> {
    const response = await this.client.get<WorldModel>(`/scans/${scanId}/world-model`);
    return response.data;
  }

  // Wheelchair Profiles
  async listWheelchairProfiles(): Promise<WheelchairProfile[]> {
    const response = await this.client.get<WheelchairProfile[]>('/wheelchair-profiles');
    return response.data;
  }

  async createWheelchairProfile(
    data: Omit<WheelchairProfile, 'id' | 'is_default'>
  ): Promise<WheelchairProfile> {
    const response = await this.client.post<WheelchairProfile>(
      '/wheelchair-profiles',
      data
    );
    return response.data;
  }

  async getWheelchairProfile(profileId: string): Promise<WheelchairProfile> {
    const response = await this.client.get<WheelchairProfile>(
      `/wheelchair-profiles/${profileId}`
    );
    return response.data;
  }

  async deleteWheelchairProfile(profileId: string): Promise<void> {
    await this.client.delete(`/wheelchair-profiles/${profileId}`);
  }
}

export const api = new ApiClient();
