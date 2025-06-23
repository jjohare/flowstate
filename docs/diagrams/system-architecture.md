# System Architecture Diagrams

This document contains detailed architectural diagrams for the Tai Chi Motion Capture Application, illustrating the system's structure, data flow, and component relationships.

## High-Level System Architecture

```mermaid
C4Context
    title System Context Diagram for Tai Chi Motion Capture Application

    Person(practitioner, "Tai Chi Practitioner", "Uses the application to study movements")
    Person(instructor, "Instructor", "Analyzes student performances")
    
    System(taichiApp, "Tai Chi Motion Capture App", "Desktop application for 3D visualization of Tai Chi movements")
    
    System_Ext(videoProcessor, "Video Processing System", "Extracts pose data from videos")
    System_Ext(fileSystem, "File System", "Stores animation JSON files")
    
    Rel(practitioner, taichiApp, "Views animations, practices forms")
    Rel(instructor, taichiApp, "Analyzes movements, teaches")
    Rel(videoProcessor, fileSystem, "Exports JSON data")
    Rel(taichiApp, fileSystem, "Loads animation files")
```

## Container Architecture

```mermaid
C4Container
    title Container Diagram for Tai Chi Motion Capture Application

    Person(user, "User", "Practitioner or Instructor")
    
    Container_Boundary(desktop, "Desktop Application") {
        Container(electronMain, "Electron Main Process", "Node.js", "Manages application lifecycle, file access")
        Container(electronRenderer, "Electron Renderer", "Chromium", "Runs the web application")
        Container(reactApp, "React Application", "React/TypeScript", "User interface and interaction")
        Container(threeJS, "Three.js Engine", "WebGL", "3D rendering and animation")
    }
    
    System_Ext(fs, "File System", "JSON animation files")
    
    Rel(user, electronRenderer, "Interacts with", "UI events")
    Rel(electronRenderer, reactApp, "Hosts")
    Rel(reactApp, threeJS, "Uses", "3D rendering")
    Rel(electronMain, electronRenderer, "IPC communication")
    Rel(electronMain, fs, "File I/O")
```

## Component Architecture

```mermaid
C4Component
    title Component Diagram for React Application

    Container_Boundary(reactApp, "React Application") {
        Component(app, "App", "React Component", "Root component, manages data loading")
        Component(animViewer, "AnimationViewer", "React Component", "Main viewer interface")
        Component(stickFigure, "StickFigure", "React/Three.js", "3D figure renderer")
        Component(controls, "PlaybackControls", "React Component", "Animation controls")
        Component(timeline, "Timeline", "React Component", "Frame navigation")
        Component(camera, "CameraControls", "Three.js", "3D camera management")
        
        Component(loader, "AnimationLoader", "TypeScript Class", "File loading and validation")
        Component(processor, "AnimationProcessor", "TypeScript Class", "Data optimization")
        Component(utils, "PoseConnections", "Utilities", "Skeletal structure definitions")
    }
    
    Rel(app, animViewer, "Renders")
    Rel(app, loader, "Uses", "Load data")
    Rel(animViewer, stickFigure, "Contains")
    Rel(animViewer, controls, "Contains")
    Rel(animViewer, camera, "Contains")
    Rel(controls, timeline, "Contains")
    Rel(stickFigure, utils, "Uses", "Connections")
    Rel(loader, processor, "May use", "Optimization")
```

## Data Flow Architecture

```mermaid
graph TB
    subgraph "Data Source"
        VF[Video File]
        VP[Video Processor]
        JF[JSON File]
    end
    
    subgraph "Electron App"
        subgraph "Main Process"
            FS[File System API]
            IPC[IPC Handler]
        end
        
        subgraph "Renderer Process"
            subgraph "Data Layer"
                AL[AnimationLoader]
                VD[Validation]
                AP[AnimationProcessor]
            end
            
            subgraph "State Layer"
                RS[React State]
                PS[Playback State]
            end
            
            subgraph "Presentation Layer"
                T3[Three.js Scene]
                UI[UI Components]
            end
        end
    end
    
    VF --> VP
    VP --> JF
    JF --> FS
    FS --> IPC
    IPC --> AL
    AL --> VD
    VD --> AP
    AP --> RS
    RS --> PS
    PS --> T3
    PS --> UI
    
    style VP fill:#f96,stroke:#333,stroke-width:2px
    style T3 fill:#6f9,stroke:#333,stroke-width:2px
```

## Rendering Pipeline

```mermaid
graph LR
    subgraph "Frame Data"
        FD[Frame Data]
        PL[Pose Landmarks]
        HD[Hand Data]
    end
    
    subgraph "Coordinate Transform"
        NC[Normalize Coords]
        WC[World Coords]
        SC[Scene Coords]
    end
    
    subgraph "3D Objects"
        JM[Joint Meshes]
        BL[Bone Lines]
        HM[Hand Meshes]
    end
    
    subgraph "Three.js"
        SG[Scene Graph]
        CM[Camera]
        LT[Lights]
        RD[Renderer]
    end
    
    subgraph "Output"
        CV[Canvas]
        WG[WebGL Context]
    end
    
    FD --> PL
    FD --> HD
    PL --> NC
    HD --> NC
    NC --> WC
    WC --> SC
    SC --> JM
    SC --> BL
    SC --> HM
    JM --> SG
    BL --> SG
    HM --> SG
    CM --> RD
    LT --> RD
    SG --> RD
    RD --> CV
    CV --> WG
```

## State Management Flow

```mermaid
stateDiagram-v2
    [*] --> AppLoading: Application Start
    
    AppLoading --> DataLoaded: Load Success
    AppLoading --> ErrorState: Load Failed
    
    DataLoaded --> Ready: Initialize Viewer
    
    Ready --> Playing: User Clicks Play
    Ready --> FrameSeeking: User Drags Timeline
    
    Playing --> Paused: User Clicks Pause
    Playing --> FrameAdvancing: Animation Loop
    Playing --> Ready: User Clicks Stop
    
    Paused --> Playing: User Clicks Play
    Paused --> Ready: User Clicks Stop
    Paused --> FrameSeeking: User Drags Timeline
    
    FrameAdvancing --> Playing: Next Frame
    FrameAdvancing --> Ready: Last Frame
    
    FrameSeeking --> Ready: Release Drag
    
    state Playing {
        [*] --> AnimationLoop
        AnimationLoop --> CalculateFrame
        CalculateFrame --> UpdateState
        UpdateState --> RenderFrame
        RenderFrame --> AnimationLoop: Continue
    }
```

## IPC Communication Architecture

```mermaid
sequenceDiagram
    participant U as User
    participant R as Renderer Process
    participant I as IPC
    participant M as Main Process
    participant F as File System
    
    U->>R: Click "Open File"
    R->>I: Send 'open-file-dialog'
    I->>M: Handle IPC message
    M->>M: Show file dialog
    M->>F: User selects file
    F->>M: File path
    M->>F: Read file content
    F->>M: JSON data
    M->>I: Send file data
    I->>R: Receive data
    R->>R: Validate & parse
    R->>R: Update state
    R->>U: Display animation
```

## Module Dependency Graph

```mermaid
graph TD
    subgraph "External Dependencies"
        E[Electron]
        R[React]
        T[Three.js]
        RTF[@react-three/fiber]
        RTD[@react-three/drei]
        TS[TypeScript]
    end
    
    subgraph "Application Core"
        APP[App.tsx]
        IDX[index.tsx]
    end
    
    subgraph "Components"
        AV[AnimationViewer]
        SF[StickFigure]
        PC[PlaybackControls]
        TL[Timeline]
        CC[CameraControls]
    end
    
    subgraph "Utilities"
        AL[AnimationLoader]
        AP[AnimationProcessor]
        PS[PoseConnections]
    end
    
    subgraph "Types"
        TY[types/index.ts]
    end
    
    E --> APP
    R --> IDX
    R --> APP
    R --> AV
    T --> SF
    RTF --> AV
    RTF --> SF
    RTD --> AV
    TS --> TY
    
    IDX --> APP
    APP --> AV
    AV --> SF
    AV --> PC
    AV --> CC
    PC --> TL
    
    APP --> AL
    AL --> TY
    AP --> TY
    SF --> PS
    PS --> TY
    
    style E fill:#61dafb,stroke:#333,stroke-width:2px
    style R fill:#61dafb,stroke:#333,stroke-width:2px
    style T fill:#049ef4,stroke:#333,stroke-width:2px
```

## Performance Architecture

```mermaid
graph TD
    subgraph "Optimization Layers"
        subgraph "Data Layer"
            DC[Data Compression]
            PC[Precision Control]
            FI[Frame Interpolation]
        end
        
        subgraph "Rendering Layer"
            IM[Instanced Meshes]
            FC[Frustum Culling]
            LOD[Level of Detail]
        end
        
        subgraph "React Layer"
            ME[React.memo]
            UC[useCallback]
            UM[useMemo]
        end
    end
    
    subgraph "Performance Metrics"
        FPS[60 FPS Target]
        MU[Memory < 200MB]
        LT[Load Time < 2s]
    end
    
    DC --> FPS
    PC --> MU
    FI --> FPS
    IM --> FPS
    FC --> FPS
    LOD --> FPS
    ME --> MU
    UC --> MU
    UM --> MU
    
    style FPS fill:#6f9,stroke:#333,stroke-width:2px
    style MU fill:#6f9,stroke:#333,stroke-width:2px
    style LT fill:#6f9,stroke:#333,stroke-width:2px
```

## Security Architecture

```mermaid
graph TB
    subgraph "Security Boundaries"
        subgraph "Main Process"
            FD[File Dialog Only]
            PL[Path Validation]
            SZ[Size Limits]
        end
        
        subgraph "Renderer Process"
            CI[Context Isolation]
            PS[Preload Scripts]
            CSP[Content Security Policy]
        end
        
        subgraph "Data Validation"
            JS[JSON Schema]
            TV[Type Validation]
            RV[Range Validation]
        end
    end
    
    subgraph "Attack Vectors"
        MF[Malicious Files]
        XS[XSS Attempts]
        PE[Path Exploits]
    end
    
    MF -.->|Blocked| FD
    MF -.->|Blocked| SZ
    XS -.->|Blocked| CSP
    XS -.->|Blocked| CI
    PE -.->|Blocked| PL
    
    FD --> JS
    JS --> TV
    TV --> RV
    
    style MF fill:#f66,stroke:#333,stroke-width:2px
    style XS fill:#f66,stroke:#333,stroke-width:2px
    style PE fill:#f66,stroke:#333,stroke-width:2px
```

## Deployment Architecture

```mermaid
graph TD
    subgraph "Source"
        SC[Source Code]
        CF[Config Files]
        AS[Assets]
    end
    
    subgraph "Build Process"
        TSC[TypeScript Compile]
        WP[Webpack Bundle]
        EB[Electron Builder]
    end
    
    subgraph "Platform Builds"
        subgraph "Windows"
            EXE[.exe Installer]
            ZIP[Portable ZIP]
        end
        
        subgraph "macOS"
            DMG[.dmg Image]
            APP[.app Bundle]
        end
        
        subgraph "Linux"
            DEB[.deb Package]
            AI[AppImage]
        end
    end
    
    subgraph "Distribution"
        GH[GitHub Releases]
        WEB[Website]
        AS2[App Stores]
    end
    
    SC --> TSC
    CF --> WP
    AS --> WP
    TSC --> WP
    WP --> EB
    
    EB --> EXE
    EB --> ZIP
    EB --> DMG
    EB --> APP
    EB --> DEB
    EB --> AI
    
    EXE --> GH
    DMG --> GH
    AI --> GH
    
    ZIP --> WEB
    APP --> AS2
    
    style EB fill:#f90,stroke:#333,stroke-width:2px
```

---

For implementation details, see:
- [Architecture Overview](../architecture/README.md)
- [Component Documentation](../components/README.md)
- [API Reference](../api/README.md)