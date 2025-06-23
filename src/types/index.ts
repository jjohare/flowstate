// Motion capture types
export interface Keypoint {
  x: number;
  y: number;
  z?: number;
  confidence: number;
}

export interface Pose {
  keypoints: Keypoint[];
  timestamp: number;
  frameIndex: number;
}

export interface MotionFrame {
  pose: Pose;
  flowMetrics?: FlowMetrics;
  annotations?: string[];
}

// Flow state analysis types
export interface FlowMetrics {
  coherence: number; // 0-1, movement harmony
  smoothness: number; // 0-1, transition quality
  balance: number; // 0-1, weight distribution
  energy: number; // 0-1, movement energy
  focus: number; // 0-1, attention/concentration
  timestamp: number;
}

export interface FlowSegment {
  startTime: number;
  endTime: number;
  averageMetrics: FlowMetrics;
  peakFlow: number;
  notes?: string;
}

// Training types
export interface TrainingProgram {
  id: string;
  name: string;
  description: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  duration: number; // minutes
  exercises: Exercise[];
}

export interface Exercise {
  id: string;
  name: string;
  description: string;
  duration: number; // seconds
  referenceVideo?: string;
  keyPositions: Pose[];
}

export interface TrainingSession {
  id: string;
  programId: string;
  startTime: Date;
  endTime?: Date;
  performance: {
    accuracy: number;
    completionRate: number;
    flowScore: number;
  };
  exercises: ExerciseResult[];
}

export interface ExerciseResult {
  exerciseId: string;
  completed: boolean;
  accuracy: number;
  flowMetrics: FlowMetrics;
  feedback: string[];
}

// Analysis types
export interface MovementAnalysis {
  sessionId: string;
  timestamp: Date;
  overallScore: number;
  strengths: string[];
  improvements: string[];
  flowPattern: FlowSegment[];
  recommendations: string[];
}

// Visualization types
export interface VisualizationSettings {
  showSkeleton: boolean;
  showTrajectories: boolean;
  showFlowField: boolean;
  skeletonColor: string;
  trajectoryLength: number;
  playbackSpeed: number;
}

// Export types
export interface ExportOptions {
  format: 'json' | 'csv' | 'video';
  includeAnalysis: boolean;
  includeRawData: boolean;
  quality?: 'low' | 'medium' | 'high';
}