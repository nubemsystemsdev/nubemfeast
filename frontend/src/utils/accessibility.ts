import type { AccessibilityRating, BarrierSeverity, BarrierType } from '../types';

export const SEVERITY_LABELS: Record<BarrierSeverity, string> = {
  low: 'Bajo',
  medium: 'Medio',
  high: 'Alto',
  critical: 'Critico',
};

export const SEVERITY_COLORS: Record<BarrierSeverity, string> = {
  low: 'bg-green-100 text-green-800',
  medium: 'bg-yellow-100 text-yellow-800',
  high: 'bg-orange-100 text-orange-800',
  critical: 'bg-red-100 text-red-800',
};

export const RATING_LABELS: Record<AccessibilityRating, string> = {
  accessible: 'Accesible',
  caution: 'Precaucion',
  difficult: 'Dificil',
  inaccessible: 'Inaccesible',
};

export const RATING_COLORS: Record<AccessibilityRating, string> = {
  accessible: 'bg-green-100 text-green-800 border-green-200',
  caution: 'bg-yellow-100 text-yellow-800 border-yellow-200',
  difficult: 'bg-orange-100 text-orange-800 border-orange-200',
  inaccessible: 'bg-red-100 text-red-800 border-red-200',
};

export const BARRIER_TYPE_LABELS: Record<BarrierType, string> = {
  step: 'Escalon',
  stairs: 'Escalera',
  narrow_door: 'Puerta estrecha',
  narrow_passage: 'Pasillo estrecho',
  steep_ramp: 'Rampa empinada',
  uneven_surface: 'Superficie irregular',
  obstacle: 'Obstaculo',
  heavy_door: 'Puerta pesada',
  revolving_door: 'Puerta giratoria',
  threshold: 'Umbral',
  gravel: 'Gravilla',
  grass: 'Cesped',
  slope: 'Pendiente',
  other: 'Otro',
};

export const BARRIER_TYPE_ICONS: Record<BarrierType, string> = {
  step: 'Footprints',
  stairs: 'Stairs',
  narrow_door: 'DoorClosed',
  narrow_passage: 'MoveHorizontal',
  steep_ramp: 'TrendingUp',
  uneven_surface: 'Waves',
  obstacle: 'AlertTriangle',
  heavy_door: 'Lock',
  revolving_door: 'RotateCw',
  threshold: 'MinusSquare',
  gravel: 'Circle',
  grass: 'Leaf',
  slope: 'TrendingUp',
  other: 'HelpCircle',
};

export function getAccessibilityScoreColor(score: number | null): string {
  if (score === null) return 'text-gray-400';
  if (score >= 80) return 'text-green-600';
  if (score >= 60) return 'text-yellow-600';
  if (score >= 40) return 'text-orange-600';
  return 'text-red-600';
}

export function getAccessibilityScoreLabel(score: number | null): string {
  if (score === null) return 'Sin evaluar';
  if (score >= 80) return 'Alta accesibilidad';
  if (score >= 60) return 'Accesibilidad moderada';
  if (score >= 40) return 'Accesibilidad limitada';
  return 'Accesibilidad restringida';
}
