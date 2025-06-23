export {};

declare global {
  interface Window {
    electronAPI?: {
      selectVideo: () => Promise<string | null>;
      saveSession: (data: any) => Promise<string | null>;
      loadSession: () => Promise<any | null>;
      exportVideo: (options: any) => Promise<string | null>;
      backendRequest: (endpoint: string, method: string, data?: any) => Promise<any>;
      backendHealth: () => Promise<any>;
      uploadVideo: (videoPath: string) => Promise<{ success: boolean; data?: any; error?: string }>;
      processVideo: (videoId: string) => Promise<{ success: boolean; data?: any; error?: string }>;
      getVideoStatus: (videoId: string) => Promise<{ success: boolean; data?: any; error?: string }>;
      getVideoResults: (videoId: string) => Promise<{ success: boolean; data?: any; error?: string }>;
      processStreamFrame: (frameData: string) => Promise<any>;
      getTrainingForms: () => Promise<any>;
      compareMovements: (userPoses: any, referenceForm: any) => Promise<any>;
      onBackendStatus: (callback: (status: any) => void) => void;
      onMenuAction: (action: string, callback: () => void) => void;
      onBackendReady: (callback: () => void) => void;
      platform: string;
      versions: {
        node: string;
        chrome: string;
        electron: string;
      };
    };
  }
}