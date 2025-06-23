# Architecture Overview

This document provides a comprehensive overview of the Tai Chi Motion Capture Application's architecture, including system design, component relationships, and data flow.

## System Architecture

The application follows a multi-process architecture typical of Electron applications, with clear separation between the main process and renderer process.

```mermaid
graph TB
    subgraph "Desktop Environment"
        MP[Main Process<br/>Node.js Runtime]
        RP[Renderer Process<br/>Chromium]
    end
    
    subgraph "External Data"
        VF[Video Files]
        JD[JSON Data]
        FS[File System]
    end
    
    subgraph "Application Core"
        EA[Electron App]
        RA[React App]
        T3[Three.js Engine]
    end
    
    MP --> EA
    RP --> RA
    RA --> T3
    VF --> JD
    JD --> FS
    FS --> MP
    MP -.IPC.-> RP
    
    style MP fill:#f9f,stroke:#333,stroke-width:2px
    style RP fill:#bbf,stroke:#333,stroke-width:2px
    style T3 fill:#bfb,stroke:#333,stroke-width:2px
```

## Component Architecture

The application is built using a component-based architecture with React and Three.js integration.

```mermaid
graph TD
    App[App Component]
    AV[AnimationViewer]
    SF[StickFigure]
    PC[PlaybackControls]
    TL[Timeline]
    CC[CameraControls]
    
    App --> AV
    AV --> SF
    AV --> PC
    AV --> TL
    AV --> CC
    
    subgraph "Three.js Components"
        C3[Canvas]
        OC[OrbitControls]
        GR[Grid]
        CA[Camera]
    end
    
    SF --> C3
    CC --> OC
    AV --> GR
    AV --> CA
    
    subgraph "Data Layer"
        AD[AnimationData]
        AL[AnimationLoader]
        AP[AnimationProcessor]
    end
    
    App --> AL
    AL --> AD
    AP --> AD
    SF --> AD
```

## Data Flow Architecture

The data flow follows a unidirectional pattern from video processing to 3D rendering.

```mermaid
sequenceDiagram
    participant V as Video Source
    participant P as Pose Processor
    participant J as JSON Export
    participant E as Electron App
    participant R as React Frontend
    participant T as Three.js
    participant U as User
    
    V->>P: Raw video frames
    P->>P: Extract pose landmarks
    P->>J: Export animation data
    J->>E: Load JSON file
    E->>R: Pass animation data
    R->>T: Render 3D scene
    T->>U: Display animation
    U->>R: Interact with controls
    R->>T: Update visualization
```

## Process Communication

Electron's IPC (Inter-Process Communication) enables secure communication between main and renderer processes.

```mermaid
graph LR
    subgraph "Main Process"
        MW[Main Window]
        FM[File Manager]
        MM[Menu Manager]
    end
    
    subgraph "IPC Channels"
        LC[load-animation]
        SC[save-animation]
        FC[file-dialog]
        UC[update-check]
    end
    
    subgraph "Renderer Process"
        RA[React App]
        AS[App State]
        UI[UI Components]
    end
    
    FM <--> LC <--> RA
    FM <--> SC <--> AS
    MM <--> FC <--> UI
    MW <--> UC <--> RA
    
    style LC fill:#faa,stroke:#333,stroke-width:2px
    style SC fill:#faa,stroke:#333,stroke-width:2px
    style FC fill:#faa,stroke:#333,stroke-width:2px
    style UC fill:#faa,stroke:#333,stroke-width:2px
```

## State Management

The application uses React's built-in state management with hooks for managing animation state.

```mermaid
stateDiagram-v2
    [*] --> Loading
    Loading --> Ready: Data Loaded
    Loading --> Error: Load Failed
    
    Ready --> Playing: Play
    Playing --> Paused: Pause
    Paused --> Playing: Resume
    Playing --> Ready: Stop
    Paused --> Ready: Stop
    
    Ready --> Scrubbing: Timeline Drag
    Scrubbing --> Ready: Release
    
    state Ready {
        [*] --> Idle
        Idle --> FrameUpdate: Frame Change
        FrameUpdate --> Idle
    }
    
    state Playing {
        [*] --> AnimationLoop
        AnimationLoop --> FrameAdvance
        FrameAdvance --> AnimationLoop
    }
```

## 3D Rendering Pipeline

The Three.js rendering pipeline processes animation data into visual output.

```mermaid
graph TD
    AD[Animation Data]
    FD[Frame Data]
    PL[Pose Landmarks]
    WC[World Coordinates]
    SG[Scene Graph]
    GE[Geometries]
    MA[Materials]
    ME[Meshes]
    RE[Renderer]
    SC[Screen]
    
    AD --> FD
    FD --> PL
    PL --> WC
    WC --> SG
    SG --> GE
    SG --> MA
    GE --> ME
    MA --> ME
    ME --> RE
    RE --> SC
    
    subgraph "Optimization"
        IM[Instanced Meshes]
        BG[Buffer Geometry]
        FC[Frustum Culling]
    end
    
    ME --> IM
    GE --> BG
    RE --> FC
```

## Module Dependencies

The application's module structure and dependencies.

```mermaid
graph BT
    subgraph "External Dependencies"
        R[React]
        E[Electron]
        T[Three.js]
        RTF[React Three Fiber]
        RTD[React Three Drei]
    end
    
    subgraph "Application Modules"
        APP[App.tsx]
        AV[AnimationViewer]
        SF[StickFigure]
        UTIL[Utils]
        TYPES[Types]
    end
    
    APP --> R
    APP --> E
    AV --> R
    AV --> RTF
    SF --> T
    SF --> RTF
    SF --> RTD
    UTIL --> TYPES
    AV --> UTIL
    SF --> UTIL
```

## Deployment Architecture

The application packaging and deployment structure for different platforms.

```mermaid
graph TD
    SC[Source Code]
    BC[Build Configuration]
    EB[Electron Builder]
    
    SC --> BC
    BC --> EB
    
    EB --> WIN[Windows Build]
    EB --> MAC[macOS Build]
    EB --> LIN[Linux Build]
    
    WIN --> NSIS[NSIS Installer]
    MAC --> DMG[DMG Package]
    LIN --> AI[AppImage]
    
    NSIS --> WD[Windows Distribution]
    DMG --> MD[macOS Distribution]
    AI --> LD[Linux Distribution]
    
    subgraph "Distribution Channels"
        GH[GitHub Releases]
        AS[App Store]
        WS[Website]
    end
    
    WD --> GH
    MD --> GH
    LD --> GH
    MD --> AS
    WD --> WS
    MD --> WS
    LD --> WS
```

## Security Architecture

Security considerations and implementation.

```mermaid
graph TD
    subgraph "Security Layers"
        CSP[Content Security Policy]
        CTX[Context Isolation]
        PRE[Preload Scripts]
        SBX[Sandbox Mode]
    end
    
    subgraph "IPC Security"
        VAL[Input Validation]
        SAN[Data Sanitization]
        WHT[Channel Whitelist]
    end
    
    subgraph "File Access"
        DLG[Dialog API Only]
        RST[Restricted Paths]
        VAL2[File Validation]
    end
    
    CSP --> CTX
    CTX --> PRE
    PRE --> SBX
    
    VAL --> SAN
    SAN --> WHT
    
    DLG --> RST
    RST --> VAL2
```

## Performance Optimization

Key performance optimization strategies implemented in the application.

```mermaid
graph LR
    subgraph "Rendering Optimizations"
        IM[Instanced Meshes]
        LOD[Level of Detail]
        FC[Frustum Culling]
        BP[Batch Processing]
    end
    
    subgraph "Data Optimizations"
        DC[Data Compression]
        FI[Frame Interpolation]
        LZ[Lazy Loading]
        CA[Caching]
    end
    
    subgraph "UI Optimizations"
        RM[React.memo]
        UC[useCallback]
        UM[useMemo]
        TH[Throttling]
    end
    
    IM --> BP
    DC --> LZ
    RM --> UC
    UC --> UM
    UM --> TH
```

## Error Handling Architecture

Comprehensive error handling and recovery mechanisms.

```mermaid
stateDiagram-v2
    [*] --> Normal
    
    Normal --> FileError: File Load Failed
    Normal --> DataError: Invalid Data
    Normal --> RenderError: Render Failed
    
    FileError --> Recovery: Retry/Cancel
    DataError --> Recovery: Validate/Fix
    RenderError --> Recovery: Fallback Renderer
    
    Recovery --> Normal: Success
    Recovery --> ErrorState: Failed
    
    ErrorState --> [*]: User Action
    
    state Recovery {
        [*] --> Attempting
        Attempting --> Success
        Attempting --> Failed
    }
```

---

For more detailed information about specific components, see:
- [Component Documentation](../components/README.md)
- [API Reference](../api/README.md)
- [Data Models](../api/data-models.md)