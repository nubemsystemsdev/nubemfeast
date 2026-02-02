import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../services/api';
import { SCAN_QUERY_KEYS } from './useScans';

export const ANALYSIS_QUERY_KEYS = {
  all: ['analysis'] as const,
  detail: (scanId: string) => [...ANALYSIS_QUERY_KEYS.all, scanId] as const,
  barriers: (scanId: string) => [...ANALYSIS_QUERY_KEYS.all, scanId, 'barriers'] as const,
};

export function useAnalysis(scanId: string) {
  return useQuery({
    queryKey: ANALYSIS_QUERY_KEYS.detail(scanId),
    queryFn: () => api.getAnalysis(scanId),
    enabled: !!scanId,
    retry: false,
  });
}

export function useStartAnalysis() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      scanId,
      options,
    }: {
      scanId: string;
      options?: { wheelchair_profile_id?: string; force?: boolean };
    }) => api.startAnalysis(scanId, options),
    onSuccess: (_, { scanId }) => {
      queryClient.invalidateQueries({ queryKey: SCAN_QUERY_KEYS.detail(scanId) });
      queryClient.invalidateQueries({ queryKey: ANALYSIS_QUERY_KEYS.detail(scanId) });
    },
  });
}

export function useBarriers(scanId: string) {
  return useQuery({
    queryKey: ANALYSIS_QUERY_KEYS.barriers(scanId),
    queryFn: () => api.listBarriers(scanId),
    enabled: !!scanId,
  });
}
