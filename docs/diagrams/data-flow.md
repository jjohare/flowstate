# Data Flow Diagrams

This document illustrates the complete data flow within the Tai Chi Motion Capture Application, from video processing to 3D visualization.

## End-to-End Data Pipeline

```mermaid
graph TB
    subgraph "Data Creation"
        V[Video Recording]
        ML[ML Processing]
        PE[Pose Extraction]
        JE[JSON Export]
    end
    
    subgraph "Data Storage"
        FS[File System]
        JF[JSON Files]
    end
    
    subgraph "Application Pipeline"
        subgraph "Loading Phase"
            FD[File Dialog]
            FR[File Read]
            JP[JSON Parse]
            VL[Validation]
        end
        
        subgraph "Processing Phase"
            DT[Data Transform]
            OPT[Optimization]
            ST[State Update]
        end
        
        subgraph "Rendering Phase"
            FC[Frame Calculate]
            CT[Coordinate Transform]
            GU[Geometry Update]
            RN[Render]
        end
    end
    
    V --> ML
    ML --> PE
    PE --> JE
    JE --> FS
    FS --> JF
    
    JF --> FD
    FD --> FR
    FR --> JP
    JP --> VL
    VL --> DT
    DT --> OPT
    OPT --> ST
    
    ST --> FC
    FC --> CT
    CT --> GU
    GU --> RN
    
    style ML fill:#f96,stroke:#333,stroke-width:2px
    style VL fill:#6f9,stroke:#333,stroke-width:2px
    style RN fill:#69f,stroke:#333,stroke-width:2px
```

## Animation Data Lifecycle

```mermaid
sequenceDiagram
    participant User
    participant FileSystem
    participant Electron
    participant Loader
    participant Validator
    participant State
    participant Renderer
    participant Three.js
    
    User->>Electron: Open File
    Electron->>FileSystem: Show Dialog
    FileSystem->>Electron: File Path
    Electron->>FileSystem: Read File
    FileSystem->>Electron: JSON Content
    Electron->>Loader: Pass Data
    Loader->>Validator: Validate Structure
    
    alt Valid Data
        Validator->>Loader: Success
        Loader->>State: Update AnimationData
        State->>Renderer: Trigger Re-render
        Renderer->>Three.js: Update Scene
        Three.js->>User: Display Animation
    else Invalid Data
        Validator->>Loader: Error
        Loader->>User: Show Error Message
    end
```

## Frame Processing Pipeline

```mermaid
graph LR
    subgraph "Input Data"
        FN[Frame Number]
        AD[Animation Data]
        PS[Playback State]
    end
    
    subgraph "Frame Selection"
        CI[Calculate Index]
        GF[Get Frame Data]
        IL[Interpolate if Needed]
    end
    
    subgraph "Landmark Processing"
        PL[Pose Landmarks]
        HL[Hand Landmarks]
        VF[Visibility Flags]
    end
    
    subgraph "Coordinate Transformation"
        NC[Normalize Coordinates]
        MC[Mirror Coordinates]
        SC[Scale to Scene]
    end
    
    subgraph "3D Objects"
        JO[Joint Objects]
        BO[Bone Objects]
        HO[Hand Objects]
    end
    
    FN --> CI
    AD --> GF
    PS --> CI
    CI --> GF
    GF --> IL
    IL --> PL
    IL --> HL
    IL --> VF
    
    PL --> NC
    HL --> NC
    NC --> MC
    MC --> SC
    
    SC --> JO
    SC --> BO
    SC --> HO
    
    style CI fill:#f9f,stroke:#333,stroke-width:2px
    style SC fill:#9ff,stroke:#333,stroke-width:2px
```

## State Management Flow

```mermaid
stateDiagram-v2
    [*] --> Initial
    
    Initial --> Loading: Load Animation
    Loading --> Loaded: Success
    Loading --> Error: Failure
    Error --> Initial: Reset
    
    Loaded --> Ready: Initialize
    
    state Ready {
        [*] --> Idle
        Idle --> Playing: Play
        Idle --> Seeking: Seek
        
        Playing --> Paused: Pause
        Playing --> Idle: Stop
        Paused --> Playing: Resume
        Paused --> Idle: Stop
        
        Seeking --> Idle: Release
    }
    
    state Playing {
        [*] --> FrameLoop
        FrameLoop --> UpdateFrame
        UpdateFrame --> CheckEnd
        CheckEnd --> FrameLoop: Continue
        CheckEnd --> [*]: End
    }
```

## Coordinate System Transformations

```mermaid
graph TD
    subgraph "Video Space"
        VS[0-1 Normalized<br/>Origin: Top-Left<br/>Y-Down]
    end
    
    subgraph "World Space"
        WS[Metric Units<br/>Origin: Center<br/>Y-Up]
    end
    
    subgraph "Scene Space"
        SS[Three.js Units<br/>Origin: Center<br/>Y-Up]
    end
    
    subgraph "Screen Space"
        SC[Pixel Coordinates<br/>Origin: Top-Left<br/>Y-Down]
    end
    
    VS -->|Transform| WS
    WS -->|Scale| SS
    SS -->|Project| SC
    
    subgraph "Transformations"
        T1["X' = (X - 0.5) * 2"]
        T2["Y' = -(Y - 0.5) * 2"]
        T3["Z' = -Z * 2"]
        T4["Mirror: X' = -X'"]
    end
    
    VS --> T1
    VS --> T2
    VS --> T3
    T1 --> WS
    T2 --> WS
    T3 --> WS
    WS --> T4
```

## IPC Data Flow

```mermaid
graph TB
    subgraph "Renderer Process"
        UI[UI Events]
        RC[React Components]
        IH[IPC Handler]
    end
    
    subgraph "IPC Channels"
        C1[load-animation]
        C2[save-animation]
        C3[export-frame]
        C4[app-settings]
    end
    
    subgraph "Main Process"
        MH[Message Handler]
        FA[File Access]
        WM[Window Manager]
        SM[Settings Manager]
    end
    
    UI --> RC
    RC --> IH
    
    IH --> C1
    IH --> C2
    IH --> C3
    IH --> C4
    
    C1 --> MH
    C2 --> MH
    C3 --> MH
    C4 --> MH
    
    MH --> FA
    MH --> WM
    MH --> SM
    
    FA --> C1
    FA --> C2
    FA --> C3
    SM --> C4
    
    style C1 fill:#f96,stroke:#333,stroke-width:2px
    style C2 fill:#f96,stroke:#333,stroke-width:2px
    style C3 fill:#f96,stroke:#333,stroke-width:2px
    style C4 fill:#f96,stroke:#333,stroke-width:2px
```

## Performance Data Flow

```mermaid
graph LR
    subgraph "Data Input"
        RD[Raw Data<br/>~10MB]
    end
    
    subgraph "Optimization Pipeline"
        PR[Precision Reduction<br/>4 decimals]
        FC[Frame Culling<br/>Remove duplicates]
        DC[Data Compression<br/>Remove nulls]
    end
    
    subgraph "Memory Management"
        BP[Buffer Pool<br/>Reuse objects]
        GC[Garbage Collection<br/>Scheduled cleanup]
        LZ[Lazy Loading<br/>On-demand frames]
    end
    
    subgraph "Rendering Pipeline"
        IM[Instanced Meshes<br/>Single draw call]
        FC2[Frustum Culling<br/>Skip off-screen]
        LOD[Level of Detail<br/>Distance-based]
    end
    
    subgraph "Output"
        OP[Optimized<br/>~2MB]
        FPS[60 FPS]
    end
    
    RD --> PR
    PR --> FC
    FC --> DC
    DC --> BP
    BP --> GC
    GC --> LZ
    LZ --> IM
    IM --> FC2
    FC2 --> LOD
    LOD --> OP
    LOD --> FPS
    
    style RD fill:#f66,stroke:#333,stroke-width:2px
    style OP fill:#6f6,stroke:#333,stroke-width:2px
    style FPS fill:#6f6,stroke:#333,stroke-width:2px
```

## Error Handling Flow

```mermaid
flowchart TD
    Start[Data Operation]
    
    TRY[Try Operation]
    
    E1[File Error]
    E2[Parse Error]
    E3[Validation Error]
    E4[Render Error]
    
    H1[Show File Dialog]
    H2[Display Parse Error]
    H3[Show Validation Details]
    H4[Fallback Renderer]
    
    R1[Retry Operation]
    R2[Load Default]
    R3[Skip Frame]
    R4[Reset View]
    
    Success[Continue]
    
    Start --> TRY
    
    TRY --> E1
    TRY --> E2
    TRY --> E3
    TRY --> E4
    TRY --> Success
    
    E1 --> H1 --> R1
    E2 --> H2 --> R2
    E3 --> H3 --> R3
    E4 --> H4 --> R4
    
    R1 --> TRY
    R2 --> Success
    R3 --> Success
    R4 --> Success
    
    style E1 fill:#f99,stroke:#333,stroke-width:2px
    style E2 fill:#f99,stroke:#333,stroke-width:2px
    style E3 fill:#f99,stroke:#333,stroke-width:2px
    style E4 fill:#f99,stroke:#333,stroke-width:2px
```

## Data Validation Pipeline

```mermaid
graph TD
    subgraph "Input Validation"
        IV[Input Data]
        FT[File Type Check]
        SZ[Size Check]
        JS[JSON Parse]
    end
    
    subgraph "Schema Validation"
        MD[Metadata Check]
        SK[Skeleton Check]
        FR[Frames Check]
    end
    
    subgraph "Data Validation"
        RG[Range Check]
        CN[Connections Valid]
        LN[Landmark Count]
    end
    
    subgraph "Output"
        VD[Valid Data]
        ER[Error Report]
    end
    
    IV --> FT
    FT -->|Pass| SZ
    FT -->|Fail| ER
    SZ -->|Pass| JS
    SZ -->|Fail| ER
    JS -->|Pass| MD
    JS -->|Fail| ER
    
    MD -->|Pass| SK
    MD -->|Fail| ER
    SK -->|Pass| FR
    SK -->|Fail| ER
    FR -->|Pass| RG
    FR -->|Fail| ER
    
    RG -->|Pass| CN
    RG -->|Fail| ER
    CN -->|Pass| LN
    CN -->|Fail| ER
    LN -->|Pass| VD
    LN -->|Fail| ER
    
    style VD fill:#6f9,stroke:#333,stroke-width:2px
    style ER fill:#f96,stroke:#333,stroke-width:2px
```

## Real-time Update Flow

```mermaid
sequenceDiagram
    participant Timer
    participant AnimationLoop
    participant State
    participant FrameCalculator
    participant Renderer
    participant GPU
    participant Display
    
    Timer->>AnimationLoop: RequestAnimationFrame
    
    AnimationLoop->>State: Check Playing
    
    alt Is Playing
        AnimationLoop->>FrameCalculator: Calculate Next Frame
        FrameCalculator->>FrameCalculator: Apply Speed Multiplier
        FrameCalculator->>State: Update Current Frame
        
        State->>Renderer: Trigger Update
        Renderer->>Renderer: Process Frame Data
        Renderer->>Renderer: Update Geometries
        Renderer->>GPU: Submit Draw Calls
        GPU->>Display: Render Frame
        
        Display->>Timer: VSync Signal
    else Not Playing
        AnimationLoop->>Timer: Skip Frame
    end
    
    Timer->>AnimationLoop: Next Frame
```

---

For more details, see:
- [System Architecture](./system-architecture.md)
- [API Reference](../api/README.md)
- [Component Documentation](../components/README.md)