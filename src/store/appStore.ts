import { create } from 'zustand';
import { devtools } from 'zustand/middleware';

interface BackendStatus {
  status: 'idle' | 'running' | 'error' | 'stopped';
  message?: string;
  code?: number;
}

interface Session {
  id: string;
  timestamp: Date;
  videoPath?: string;
  motionData?: any[];
  flowMetrics?: any;
  analysis?: any;
}

interface AppState {
  // Backend status
  backendStatus: BackendStatus;
  setBackendStatus: (status: BackendStatus) => void;
  
  // Session management
  currentSession: Session | null;
  sessions: Session[];
  createSession: () => void;
  loadSession: (session: Session) => void;
  saveSession: () => Promise<void>;
  
  // Video state
  videoPath: string | null;
  setVideoPath: (path: string | null) => void;
  isProcessing: boolean;
  setIsProcessing: (processing: boolean) => void;
  processingProgress: number;
  setProcessingProgress: (progress: number) => void;
  
  // Motion capture data
  motionData: any[];
  setMotionData: (data: any[]) => void;
  currentFrame: number;
  setCurrentFrame: (frame: number) => void;
  
  // Flow state metrics
  flowMetrics: {
    coherence: number;
    smoothness: number;
    balance: number;
    energy: number;
    focus: number;
  };
  updateFlowMetrics: (metrics: Partial<AppState['flowMetrics']>) => void;
  
  // Settings
  settings: {
    theme: 'light' | 'dark';
    showSkeleton: boolean;
    showTrajectories: boolean;
    playbackSpeed: number;
    autoDetectFlow: boolean;
  };
  updateSettings: (settings: Partial<AppState['settings']>) => void;
  
  // App lifecycle
  initializeApp: () => void;
  resetApp: () => void;
}

export const useAppStore = create<AppState>()(devtools((set, get) => ({
  // Backend status
  backendStatus: { status: 'idle' },
  setBackendStatus: (status) => set({ backendStatus: status }),
  
  // Session management
  currentSession: null,
  sessions: [],
  createSession: () => {
    const session: Session = {
      id: Date.now().toString(),
      timestamp: new Date(),
    };
    set({ currentSession: session });
  },
  
  loadSession: (session) => set({ currentSession: session }),
  
  saveSession: async () => {
    const { currentSession } = get();
    if (!currentSession || !window.electronAPI) return;
    
    const savedPath = await window.electronAPI.saveSession(currentSession);
    if (savedPath) {
      console.log('Session saved to:', savedPath);
    }
  },
  
  // Video state
  videoPath: null,
  setVideoPath: (path) => set({ videoPath: path }),
  isProcessing: false,
  setIsProcessing: (processing) => set({ isProcessing: processing }),
  processingProgress: 0,
  setProcessingProgress: (progress) => set({ processingProgress: progress }),
  
  // Motion capture data
  motionData: [],
  setMotionData: (data) => set({ motionData: data }),
  currentFrame: 0,
  setCurrentFrame: (frame) => set({ currentFrame: frame }),
  
  // Flow state metrics
  flowMetrics: {
    coherence: 0,
    smoothness: 0,
    balance: 0,
    energy: 0,
    focus: 0,
  },
  updateFlowMetrics: (metrics) => set((state) => ({
    flowMetrics: { ...state.flowMetrics, ...metrics }
  })),
  
  // Settings
  settings: {
    theme: 'dark',
    showSkeleton: true,
    showTrajectories: true,
    playbackSpeed: 1,
    autoDetectFlow: true,
  },
  updateSettings: (newSettings) => set((state) => ({
    settings: { ...state.settings, ...newSettings }
  })),
  
  // App lifecycle
  initializeApp: () => {
    // Load saved settings from localStorage
    const savedSettings = localStorage.getItem('taiChiFlowSettings');
    if (savedSettings) {
      set({ settings: JSON.parse(savedSettings) });
    }
    
    // Create initial session
    get().createSession();
  },
  
  resetApp: () => {
    set({
      currentSession: null,
      videoPath: null,
      isProcessing: false,
      processingProgress: 0,
      motionData: [],
      currentFrame: 0,
      flowMetrics: {
        coherence: 0,
        smoothness: 0,
        balance: 0,
        energy: 0,
        focus: 0,
      },
    });
    get().createSession();
  },
}), { name: 'tai-chi-flow-store' }));