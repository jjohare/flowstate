# Data Models Documentation

This document provides detailed information about the data structures used in the Tai Chi Motion Capture Application, including the animation data format, pose landmark definitions, and skeletal connections.

## Animation Data Structure

The animation data follows a hierarchical JSON structure designed for efficient storage and processing of motion capture data.

```mermaid
graph TD
    AD[AnimationData]
    MD[Metadata]
    SK[Skeleton]
    FR[Frames Array]
    
    AD --> MD
    AD --> SK
    AD --> FR
    
    MD --> FPS[fps: number]
    MD --> TF[total_frames: number]
    MD --> PS[processed_size: number]
    MD --> BB[original_bbox: number array]
    
    SK --> PC[pose_connections]
    SK --> HC[hand_connections]
    SK --> LN[landmark_names]
    
    FR --> F1[Frame 0]
    FR --> F2[Frame 1]
    FR --> FN[Frame N]
    
    F1 --> FD[Frame Data]
    FD --> FN2[frame: number]
    FD --> TM[time: number]
    FD --> LM[landmarks]
    
    LM --> PL[pose: 33 landmarks]
    LM --> WP[world_pose: 33 landmarks]
    LM --> LH[left_hand: 21 landmarks]
    LM --> RH[right_hand: 21 landmarks]
```

## Pose Landmarks

The application uses 33 pose landmarks based on the MediaPipe Pose model.

```mermaid
graph TB
    subgraph "Face Landmarks (0-10)"
        N[0: Nose]
        LEI[1: Left Eye Inner]
        LE[2: Left Eye]
        LEO[3: Left Eye Outer]
        REI[4: Right Eye Inner]
        RE[5: Right Eye]
        REO[6: Right Eye Outer]
        LEA[7: Left Ear]
        REA[8: Right Ear]
        ML[9: Mouth Left]
        MR[10: Mouth Right]
    end
    
    subgraph "Upper Body (11-22)"
        LS[11: Left Shoulder]
        RS[12: Right Shoulder]
        LE2[13: Left Elbow]
        RE2[14: Right Elbow]
        LW[15: Left Wrist]
        RW[16: Right Wrist]
        LP[17: Left Pinky]
        RP[18: Right Pinky]
        LI[19: Left Index]
        RI[20: Right Index]
        LT[21: Left Thumb]
        RT[22: Right Thumb]
    end
    
    subgraph "Lower Body (23-32)"
        LH2[23: Left Hip]
        RH2[24: Right Hip]
        LK[25: Left Knee]
        RK[26: Right Knee]
        LA[27: Left Ankle]
        RA[28: Right Ankle]
        LHE[29: Left Heel]
        RHE[30: Right Heel]
        LFI[31: Left Foot Index]
        RFI[32: Right Foot Index]
    end
```

## Skeletal Connections

The skeletal structure defines how landmarks are connected to form bones.

```mermaid
graph LR
    subgraph "Face Connections"
        FC1[0-1: Nose to Left Eye Inner]
        FC2[1-2: Left Eye Inner to Left Eye]
        FC3[2-3: Left Eye to Left Eye Outer]
        FC4[3-7: Left Eye Outer to Left Ear]
        FC5[0-4: Nose to Right Eye Inner]
        FC6[4-5: Right Eye Inner to Right Eye]
        FC7[5-6: Right Eye to Right Eye Outer]
        FC8[6-8: Right Eye Outer to Right Ear]
        FC9[9-10: Mouth Left to Mouth Right]
    end
    
    subgraph "Torso Connections"
        TC1[11-12: Left to Right Shoulder]
        TC2[11-23: Left Shoulder to Left Hip]
        TC3[12-24: Right Shoulder to Right Hip]
        TC4[23-24: Left to Right Hip]
    end
    
    subgraph "Arm Connections"
        AC1[11-13: Left Shoulder to Elbow]
        AC2[13-15: Left Elbow to Wrist]
        AC3[15-17: Left Wrist to Pinky]
        AC4[15-19: Left Wrist to Index]
        AC5[15-21: Left Wrist to Thumb]
        AC6[12-14: Right Shoulder to Elbow]
        AC7[14-16: Right Elbow to Wrist]
        AC8[16-18: Right Wrist to Pinky]
        AC9[16-20: Right Wrist to Index]
        AC10[16-22: Right Wrist to Thumb]
    end
    
    subgraph "Leg Connections"
        LC1[23-25: Left Hip to Knee]
        LC2[25-27: Left Knee to Ankle]
        LC3[27-29: Left Ankle to Heel]
        LC4[29-31: Left Heel to Foot Index]
        LC5[27-31: Left Ankle to Foot Index]
        LC6[24-26: Right Hip to Knee]
        LC7[26-28: Right Knee to Ankle]
        LC8[28-30: Right Ankle to Heel]
        LC9[30-32: Right Heel to Foot Index]
        LC10[28-32: Right Ankle to Foot Index]
    end
```

## Hand Landmarks

Each hand contains 21 landmarks forming the hand skeleton.

```mermaid
graph TD
    W[0: Wrist]
    
    subgraph "Thumb"
        T1[1: Thumb CMC]
        T2[2: Thumb MCP]
        T3[3: Thumb IP]
        T4[4: Thumb Tip]
    end
    
    subgraph "Index Finger"
        I1[5: Index MCP]
        I2[6: Index PIP]
        I3[7: Index DIP]
        I4[8: Index Tip]
    end
    
    subgraph "Middle Finger"
        M1[9: Middle MCP]
        M2[10: Middle PIP]
        M3[11: Middle DIP]
        M4[12: Middle Tip]
    end
    
    subgraph "Ring Finger"
        R1[13: Ring MCP]
        R2[14: Ring PIP]
        R3[15: Ring DIP]
        R4[16: Ring Tip]
    end
    
    subgraph "Pinky"
        P1[17: Pinky MCP]
        P2[18: Pinky PIP]
        P3[19: Pinky DIP]
        P4[20: Pinky Tip]
    end
    
    W --> T1 --> T2 --> T3 --> T4
    W --> I1 --> I2 --> I3 --> I4
    W --> M1 --> M2 --> M3 --> M4
    W --> R1 --> R2 --> R3 --> R4
    W --> P1 --> P2 --> P3 --> P4
```

## Coordinate Systems

The application uses different coordinate systems for various purposes.

```mermaid
graph LR
    subgraph "Video Coordinates"
        VC[0-1 normalized<br/>Origin: top-left]
    end
    
    subgraph "World Coordinates"
        WC[Metric units<br/>Origin: center]
    end
    
    subgraph "Three.js Scene"
        TC[-1 to 1 range<br/>Y-up, Origin: center]
    end
    
    VC -->|Transform| WC
    WC -->|Convert| TC
    
    subgraph "Transformations"
        T1[X: (x - 0.5) * 2]
        T2[Y: -(y - 0.5) * 2]
        T3[Z: -z * 2]
        T4[Mirror: x * -1]
    end
```

## Data Validation Schema

The validation process ensures data integrity and compatibility.

```mermaid
flowchart TD
    Start[Validate AnimationData]
    
    VM[Validate Metadata]
    VS[Validate Skeleton]
    VF[Validate Frames]
    
    Start --> VM
    Start --> VS
    Start --> VF
    
    VM --> VFPS{fps > 0?}
    VM --> VTF{total_frames > 0?}
    VM --> VPS{processed_size valid?}
    VM --> VBB{bbox array[4]?}
    
    VS --> VPC{pose_connections array?}
    VS --> VHC{hand_connections array?}
    VS --> VLN{landmark_names object?}
    
    VF --> VFA{frames array?}
    VF --> VFL{frames.length > 0?}
    VF --> VFF{each frame valid?}
    
    VFF --> VFN{frame number valid?}
    VFF --> VFT{time valid?}
    VFF --> VFP{pose landmarks valid?}
    
    VFPS -->|Yes| Valid
    VFPS -->|No| Invalid
    VTF -->|Yes| Valid
    VTF -->|No| Invalid
    
    Valid[Valid Data]
    Invalid[Invalid Data]
```

## Example JSON Structure

```json
{
  "metadata": {
    "fps": 30,
    "total_frames": 120,
    "processed_size": 1920,
    "original_bbox": [0, 0, 1920, 1080]
  },
  "skeleton": {
    "pose_connections": [
      [0, 1], [1, 2], [2, 3], [3, 7],
      [0, 4], [4, 5], [5, 6], [6, 8],
      [9, 10], [11, 12], [11, 13], [13, 15],
      [12, 14], [14, 16], [11, 23], [12, 24],
      [23, 24], [23, 25], [25, 27], [27, 29],
      [29, 31], [27, 31], [24, 26], [26, 28],
      [28, 30], [30, 32], [28, 32]
    ],
    "hand_connections": [
      [0, 1], [1, 2], [2, 3], [3, 4],
      [0, 5], [5, 6], [6, 7], [7, 8],
      [0, 9], [9, 10], [10, 11], [11, 12],
      [0, 13], [13, 14], [14, 15], [15, 16],
      [0, 17], [17, 18], [18, 19], [19, 20],
      [5, 9], [9, 13], [13, 17]
    ],
    "landmark_names": {
      "pose": [
        "nose", "left_eye_inner", "left_eye", "left_eye_outer",
        "right_eye_inner", "right_eye", "right_eye_outer",
        "left_ear", "right_ear", "mouth_left", "mouth_right",
        "left_shoulder", "right_shoulder", "left_elbow", "right_elbow",
        "left_wrist", "right_wrist", "left_pinky", "right_pinky",
        "left_index", "right_index", "left_thumb", "right_thumb",
        "left_hip", "right_hip", "left_knee", "right_knee",
        "left_ankle", "right_ankle", "left_heel", "right_heel",
        "left_foot_index", "right_foot_index"
      ],
      "hand": [
        "wrist", "thumb_cmc", "thumb_mcp", "thumb_ip", "thumb_tip",
        "index_finger_mcp", "index_finger_pip", "index_finger_dip", "index_finger_tip",
        "middle_finger_mcp", "middle_finger_pip", "middle_finger_dip", "middle_finger_tip",
        "ring_finger_mcp", "ring_finger_pip", "ring_finger_dip", "ring_finger_tip",
        "pinky_mcp", "pinky_pip", "pinky_dip", "pinky_tip"
      ]
    }
  },
  "frames": [
    {
      "frame": 0,
      "time": 0.0,
      "landmarks": {
        "pose": [
          [0.5, 0.3, 0.5],
          [0.48, 0.28, 0.5],
          // ... 31 more landmarks
        ],
        "world_pose": [
          [0.0, 0.4, 0.0, 0.99],
          [-0.04, 0.44, 0.0, 0.98],
          // ... 31 more landmarks with visibility
        ],
        "left_hand": null,
        "right_hand": null
      }
    }
    // ... more frames
  ]
}
```

## Performance Considerations

### Data Size Optimization

```mermaid
graph TD
    O[Original Data]
    P1[Precision Reduction]
    P2[Frame Sampling]
    P3[Compression]
    
    O --> P1
    P1 --> P2
    P2 --> P3
    
    P1 --> R1[4 decimal places]
    P2 --> R2[Skip redundant frames]
    P3 --> R3[gzip compression]
    
    subgraph "Size Reduction"
        S1[100MB → 40MB]
        S2[40MB → 20MB]
        S3[20MB → 5MB]
    end
    
    R1 --> S1
    R2 --> S2
    R3 --> S3
```

### Memory Management

```mermaid
flowchart LR
    Load[Load Data]
    Parse[Parse JSON]
    Validate[Validate]
    Process[Process Frames]
    Render[Render]
    
    Load --> Parse
    Parse --> Validate
    Validate --> Process
    Process --> Render
    
    subgraph "Memory Usage"
        M1[File Buffer: ~5MB]
        M2[Parsed Object: ~20MB]
        M3[Processed Data: ~15MB]
        M4[GPU Buffers: ~10MB]
    end
    
    Load --> M1
    Parse --> M2
    Process --> M3
    Render --> M4
```

---

For more information, see:
- [API Reference](./README.md)
- [Architecture Overview](../architecture/README.md)
- [Usage Guide](../guides/usage.md)