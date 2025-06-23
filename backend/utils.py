"""Utility functions for backend operations."""

import os
import json
import numpy as np
from typing import List, Dict, Any, Tuple
import cv2
import base64
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


def encode_frame_to_base64(frame: np.ndarray) -> str:
    """Encode OpenCV frame to base64 string."""
    _, buffer = cv2.imencode('.jpg', frame)
    frame_base64 = base64.b64encode(buffer).decode('utf-8')
    return f"data:image/jpeg;base64,{frame_base64}"


def decode_base64_to_frame(base64_string: str) -> np.ndarray:
    """Decode base64 string to OpenCV frame."""
    # Remove data URL prefix if present
    if ',' in base64_string:
        base64_string = base64_string.split(',')[1]
    
    # Decode base64
    frame_bytes = base64.b64decode(base64_string)
    nparr = np.frombuffer(frame_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    return frame


def calculate_fps(timestamps: List[float]) -> float:
    """Calculate average FPS from timestamps."""
    if len(timestamps) < 2:
        return 0.0
    
    time_diffs = np.diff(timestamps)
    avg_diff = np.mean(time_diffs)
    
    if avg_diff > 0:
        return 1.0 / avg_diff
    return 0.0


def normalize_landmarks(landmarks: List[Dict[str, float]], 
                       width: int, height: int) -> List[Dict[str, float]]:
    """Convert normalized landmarks to pixel coordinates."""
    pixel_landmarks = []
    
    for landmark in landmarks:
        pixel_landmarks.append({
            'x': int(landmark['x'] * width),
            'y': int(landmark['y'] * height),
            'z': landmark['z'],
            'visibility': landmark['visibility']
        })
    
    return pixel_landmarks


def calculate_joint_angles(landmarks: List[Dict[str, float]], 
                          joint_triplets: List[Tuple[int, int, int]]) -> Dict[str, float]:
    """Calculate angles for specified joint triplets."""
    angles = {}
    
    for name, (p1_idx, p2_idx, p3_idx) in joint_triplets:
        if p1_idx < len(landmarks) and p2_idx < len(landmarks) and p3_idx < len(landmarks):
            p1 = landmarks[p1_idx]
            p2 = landmarks[p2_idx]  # Middle joint
            p3 = landmarks[p3_idx]
            
            # Calculate vectors
            v1 = np.array([p1['x'] - p2['x'], p1['y'] - p2['y'], p1['z'] - p2['z']])
            v2 = np.array([p3['x'] - p2['x'], p3['y'] - p2['y'], p3['z'] - p2['z']])
            
            # Calculate angle
            cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
            angle = np.arccos(np.clip(cos_angle, -1.0, 1.0))
            angles[name] = np.degrees(angle)
    
    return angles


def smooth_trajectory(points: List[Tuple[float, float]], window_size: int = 5) -> List[Tuple[float, float]]:
    """Smooth a trajectory using moving average."""
    if len(points) < window_size:
        return points
    
    smoothed = []
    for i in range(len(points)):
        start = max(0, i - window_size // 2)
        end = min(len(points), i + window_size // 2 + 1)
        
        window_points = points[start:end]
        avg_x = sum(p[0] for p in window_points) / len(window_points)
        avg_y = sum(p[1] for p in window_points) / len(window_points)
        
        smoothed.append((avg_x, avg_y))
    
    return smoothed


def create_session_data(video_info: Dict[str, Any], 
                       analysis_results: Dict[str, Any]) -> Dict[str, Any]:
    """Create session data for saving."""
    return {
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0',
        'video_info': video_info,
        'analysis': analysis_results,
        'metadata': {
            'processing_time': analysis_results.get('processing_time', 0),
            'model_versions': {
                'pose': 'mediapipe-2.3.0',
                'analysis': '1.0.0'
            }
        }
    }


def validate_pose_sequence(poses: List[Any], min_confidence: float = 0.5) -> List[Any]:
    """Validate and filter pose sequence."""
    valid_poses = []
    
    for pose in poses:
        if hasattr(pose, 'confidence') and pose.confidence >= min_confidence:
            valid_poses.append(pose)
        elif isinstance(pose, dict) and pose.get('confidence', 0) >= min_confidence:
            valid_poses.append(pose)
    
    return valid_poses


def calculate_movement_intensity(pose1: Dict[str, Any], pose2: Dict[str, Any]) -> float:
    """Calculate movement intensity between two poses."""
    if not pose1.get('landmarks') or not pose2.get('landmarks'):
        return 0.0
    
    total_movement = 0
    landmark_count = 0
    
    for i in range(min(len(pose1['landmarks']), len(pose2['landmarks']))):
        l1 = pose1['landmarks'][i]
        l2 = pose2['landmarks'][i]
        
        distance = np.sqrt(
            (l1['x'] - l2['x'])**2 +
            (l1['y'] - l2['y'])**2 +
            (l1['z'] - l2['z'])**2
        )
        
        total_movement += distance
        landmark_count += 1
    
    if landmark_count > 0:
        return total_movement / landmark_count
    return 0.0


def generate_feedback_message(quality_score: float, issues: List[str]) -> str:
    """Generate user-friendly feedback message."""
    if quality_score >= 0.9:
        base_message = "Excellent form! Your movements are very well executed."
    elif quality_score >= 0.75:
        base_message = "Good form! You're doing well with room for minor improvements."
    elif quality_score >= 0.6:
        base_message = "Fair form. Focus on the fundamentals to improve."
    else:
        base_message = "Keep practicing. Pay attention to the basic principles."
    
    if issues:
        issue_text = " Areas to focus on: " + ", ".join(issues[:3])
        return base_message + issue_text
    
    return base_message


def interpolate_missing_landmarks(poses: List[Dict[str, Any]], 
                                 max_gap: int = 5) -> List[Dict[str, Any]]:
    """Interpolate missing landmarks in pose sequence."""
    # Implementation for interpolating missing poses
    # This helps smooth out detection gaps
    return poses  # Placeholder for now


def extract_key_frames(poses: List[Any], 
                      motion_threshold: float = 0.1,
                      min_frame_distance: int = 10) -> List[int]:
    """Extract key frames from pose sequence."""
    if len(poses) < 2:
        return []
    
    key_frames = [0]  # Always include first frame
    
    for i in range(1, len(poses) - 1):
        if i - key_frames[-1] < min_frame_distance:
            continue
        
        # Calculate motion before and after this frame
        motion_before = calculate_movement_intensity(
            {'landmarks': poses[i-1].landmarks},
            {'landmarks': poses[i].landmarks}
        )
        motion_after = calculate_movement_intensity(
            {'landmarks': poses[i].landmarks},
            {'landmarks': poses[i+1].landmarks}
        )
        
        # Detect motion changes (peaks and valleys)
        if abs(motion_after - motion_before) > motion_threshold:
            key_frames.append(i)
    
    # Always include last frame
    if len(poses) - 1 not in key_frames:
        key_frames.append(len(poses) - 1)
    
    return key_frames