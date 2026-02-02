import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../services/api';
import type { ScanCreate, ScanUpdate, ScanStatus } from '../types';

export const SCAN_QUERY_KEYS = {
  all: ['scans'] as const,
  lists: () => [...SCAN_QUERY_KEYS.all, 'list'] as const,
  list: (filters: { status?: ScanStatus; limit?: number; offset?: number }) =>
    [...SCAN_QUERY_KEYS.lists(), filters] as const,
  details: () => [...SCAN_QUERY_KEYS.all, 'detail'] as const,
  detail: (id: string) => [...SCAN_QUERY_KEYS.details(), id] as const,
};

export function useScans(params?: {
  status?: ScanStatus;
  limit?: number;
  offset?: number;
}) {
  return useQuery({
    queryKey: SCAN_QUERY_KEYS.list(params || {}),
    queryFn: () => api.listScans(params),
  });
}

export function useScan(scanId: string) {
  return useQuery({
    queryKey: SCAN_QUERY_KEYS.detail(scanId),
    queryFn: () => api.getScan(scanId),
    enabled: !!scanId,
  });
}

export function useCreateScan() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: ScanCreate) => api.createScan(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: SCAN_QUERY_KEYS.lists() });
    },
  });
}

export function useUpdateScan() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ scanId, data }: { scanId: string; data: ScanUpdate }) =>
      api.updateScan(scanId, data),
    onSuccess: (_, { scanId }) => {
      queryClient.invalidateQueries({ queryKey: SCAN_QUERY_KEYS.detail(scanId) });
      queryClient.invalidateQueries({ queryKey: SCAN_QUERY_KEYS.lists() });
    },
  });
}

export function useDeleteScan() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (scanId: string) => api.deleteScan(scanId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: SCAN_QUERY_KEYS.lists() });
    },
  });
}

export function useUploadImages() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ scanId, files }: { scanId: string; files: File[] }) =>
      api.uploadImages(scanId, files),
    onSuccess: (_, { scanId }) => {
      queryClient.invalidateQueries({ queryKey: SCAN_QUERY_KEYS.detail(scanId) });
    },
  });
}

export function useDeleteImage() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({ scanId, imageId }: { scanId: string; imageId: string }) =>
      api.deleteImage(scanId, imageId),
    onSuccess: (_, { scanId }) => {
      queryClient.invalidateQueries({ queryKey: SCAN_QUERY_KEYS.detail(scanId) });
    },
  });
}
