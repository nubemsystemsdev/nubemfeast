import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { api } from '../services/api';

export const GUIDE_QUERY_KEYS = {
  all: ['guide'] as const,
  detail: (scanId: string) => [...GUIDE_QUERY_KEYS.all, scanId] as const,
  worldModel: (scanId: string) => [...GUIDE_QUERY_KEYS.all, scanId, 'world-model'] as const,
  profiles: ['wheelchair-profiles'] as const,
};

export function useGuide(scanId: string, wheelchairProfileId?: string) {
  return useQuery({
    queryKey: [...GUIDE_QUERY_KEYS.detail(scanId), wheelchairProfileId],
    queryFn: () => api.getGuide(scanId, wheelchairProfileId),
    enabled: !!scanId,
    retry: false,
  });
}

export function useGenerateGuide() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: ({
      scanId,
      wheelchairProfileId,
    }: {
      scanId: string;
      wheelchairProfileId?: string;
    }) => api.generateGuide(scanId, wheelchairProfileId),
    onSuccess: (_, { scanId }) => {
      queryClient.invalidateQueries({ queryKey: GUIDE_QUERY_KEYS.detail(scanId) });
    },
  });
}

export function useWorldModel(scanId: string) {
  return useQuery({
    queryKey: GUIDE_QUERY_KEYS.worldModel(scanId),
    queryFn: () => api.getWorldModel(scanId),
    enabled: !!scanId,
    retry: false,
  });
}

export function useWheelchairProfiles() {
  return useQuery({
    queryKey: GUIDE_QUERY_KEYS.profiles,
    queryFn: () => api.listWheelchairProfiles(),
  });
}
