// Enums
export type ScanStatus = 'pending' | 'uploading' | 'ready' | 'analyzing' | 'completed' | 'failed';
export type AnalysisStatus = 'pending' | 'in_progress' | 'completed' | 'failed';
export type BarrierType =
  | 'step'
  | 'stairs'
  | 'narrow_door'
  | 'narrow_passage'
  | 'steep_ramp'
  | 'uneven_surface'
  | 'obstacle'
  | 'heavy_door'
  | 'revolving_door'
  | 'threshold'
  | 'gravel'
  | 'grass'
  | 'slope'
  | 'other';
export type BarrierSeverity = 'low' | 'medium' | 'high' | 'critical';
export type WheelchairType = 'manual' | 'electric' | 'sport' | 'pediatric' | 'bariatric';
export type AccessibilityRating = 'accessible' | 'caution' | 'difficult' | 'inaccessible';
export type Difficulty = 'easy' | 'moderate' | 'difficult' | 'impassable';
export type SpaceType = 'entrance' | 'corridor' | 'room' | 'stairway' | 'elevator' | 'bathroom' | 'outdoor' | 'parking' | 'other';

// Scan types
export interface Scan {
  id: string;
  name: string;
  description: string | null;
  location: string | null;
  status: ScanStatus;
  image_count: number;
  created_at: string;
  updated_at: string;
}

export interface ScanDetail extends Scan {
  images: ImageInfo[];
  analysis_result: AnalysisResultSummary | null;
  has_guide: boolean;
}

export interface ScanCreate {
  name: string;
  description?: string;
  location?: string;
}

export interface ScanUpdate {
  name?: string;
  description?: string;
  location?: string;
}

// Image types
export interface ImageInfo {
  id: string;
  filename: string;
  original_filename: string;
  file_size: number;
  mime_type: string;
  width: number | null;
  height: number | null;
  sequence_order: number;
  user_description: string | null;
  created_at: string;
  barrier_count: number;
  url: string;
}

export interface ImageUploadResponse {
  uploaded: number;
  failed: number;
  images: ImageInfo[];
  errors: string[];
}

// Analysis types
export interface AnalysisResultSummary {
  status: AnalysisStatus;
  total_barriers_found: number;
  accessibility_score: number | null;
}

export interface AnalysisResponse {
  id: string;
  scan_id: string;
  status: AnalysisStatus;
  started_at: string | null;
  completed_at: string | null;
  error_message: string | null;
  total_images_analyzed: number;
  total_barriers_found: number;
  accessibility_score: number | null;
}

export interface Barrier {
  id: string;
  image_id: string;
  barrier_type: BarrierType;
  severity: BarrierSeverity;
  description: string;
  bbox_x: number | null;
  bbox_y: number | null;
  bbox_width: number | null;
  bbox_height: number | null;
  estimated_width_cm: number | null;
  estimated_height_cm: number | null;
  estimated_depth_cm: number | null;
  recommendation: string | null;
  confidence: number;
}

export interface BarrierSummary {
  id: string;
  barrier_type: BarrierType;
  severity: BarrierSeverity;
  description: string;
  recommendation: string | null;
}

// Navigation types
export interface NavigationStep {
  step_number: number;
  image_id: string;
  image_url: string;
  title: string;
  description: string;
  barriers: BarrierSummary[];
  alerts: string[];
  recommendations: string[];
  accessibility_rating: AccessibilityRating;
}

export interface Guide {
  id: string;
  scan_id: string;
  title: string;
  summary: string;
  accessibility_score: number | null;
  navigation_steps: NavigationStep[];
  critical_alerts: string[];
  wheelchair_profile: WheelchairProfile | null;
  created_at: string;
}

export interface WheelchairProfile {
  id: string;
  name: string;
  description: string | null;
  width_cm: number;
  length_cm: number;
  min_door_width_cm: number;
  max_step_height_cm: number;
  max_slope_percent: number;
  can_handle_gravel: boolean;
  can_handle_grass: boolean;
  wheelchair_type: WheelchairType;
  is_default: boolean;
}

// World Model types
export interface WorldModelNode {
  id: string;
  image_id: string;
  image_url: string;
  label: string;
  space_type: SpaceType;
  barriers: BarrierSummary[];
  accessibility_score: number;
  features: NodeFeatures;
}

export interface NodeFeatures {
  has_ramp: boolean;
  has_handrails: boolean;
  has_elevator: boolean;
  lighting: string;
  floor_type: string;
}

export interface WorldModelEdge {
  source: string;
  target: string;
  traversable: boolean;
  difficulty: Difficulty;
  barriers_in_path: string[];
  distance_estimate: 'short' | 'medium' | 'long';
  notes: string | null;
}

export interface WorldModel {
  scan_id: string;
  nodes: WorldModelNode[];
  edges: WorldModelEdge[];
  recommended_path: string[] | null;
}

// API response types
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  limit: number;
  offset: number;
}
