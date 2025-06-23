"""Video processing module for pose detection and motion analysis."""

import cv2
import numpy as np
import mediapipe as mp
from typing import List, Dict, Any, Callable, Optional
import logging
from dataclasses import dataclass
from collections import deque
import time

logger = logging.getLogger(__name__)


@dataclass
class PoseFrame:
    """Container for pose data from a single frame."""
    frame_number: int
    timestamp: float
    landmarks: Optional[List[Dict[str, float]]]
    world_landmarks: Optional[List[Dict[str, float]]]
    confidence: float
    visibility_scores: List[float]


class VideoProcessor:
    """Process videos for pose detection and motion analysis."""
    
    def __init__(self, model_manager):
        self.model_manager = model_manager
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Initialize pose detector
        self.pose_detector = None
        self.initialize_detector()
        
        # Motion tracking buffers
        self.motion_buffer = deque(maxlen=30)  # 1 second at 30fps
        self.velocity_buffer = deque(maxlen=10)
        
    def initialize_detector(self):
        """Initialize MediaPipe pose detector."""
        try:
            self.pose_detector = self.mp_pose.Pose(
                static_image_mode=False,
                model_complexity=2,  # 0, 1, or 2. Higher = more accurate but slower
                smooth_landmarks=True,
                enable_segmentation=True,
                smooth_segmentation=True,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5
            )
            logger.info("Pose detector initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize pose detector: {e}")
            raise
    
    def process_video(self, video_path: str, progress_callback: Optional[Callable] = None) -> Dict[str, Any]:
        """Process entire video file for pose detection."""
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise ValueError(f"Failed to open video: {video_path}")
        
        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        logger.info(f"Processing video: {total_frames} frames at {fps} fps")
        
        poses = []
        metrics = {
            'total_frames': total_frames,
            'frames_with_pose': 0,
            'average_confidence': 0,
            'motion_intensity': [],
            'stability_scores': []
        }
        
        frame_count = 0
        confidence_sum = 0
        
        try:
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Process frame
                pose_result = self.process_frame(frame)
                
                if pose_result['landmarks']:
                    pose_frame = PoseFrame(
                        frame_number=frame_count,
                        timestamp=frame_count / fps,
                        landmarks=pose_result['landmarks'],
                        world_landmarks=pose_result['world_landmarks'],
                        confidence=pose_result['confidence'],
                        visibility_scores=pose_result['visibility_scores']
                    )
                    poses.append(pose_frame)
                    
                    metrics['frames_with_pose'] += 1
                    confidence_sum += pose_result['confidence']
                    
                    # Calculate motion metrics
                    if len(self.motion_buffer) > 0:
                        motion_intensity = self._calculate_motion_intensity()
                        metrics['motion_intensity'].append(motion_intensity)
                
                frame_count += 1
                
                # Update progress
                if progress_callback and frame_count % 10 == 0:
                    progress = int((frame_count / total_frames) * 100)
                    progress_callback(progress)
            
            # Calculate final metrics
            if metrics['frames_with_pose'] > 0:
                metrics['average_confidence'] = confidence_sum / metrics['frames_with_pose']
            
            # Analyze motion patterns
            motion_analysis = self._analyze_motion_patterns(poses)
            
            return {
                'poses': poses,
                'metrics': metrics,
                'motion_analysis': motion_analysis,
                'frames_processed': frame_count,
                'video_info': {
                    'fps': fps,
                    'width': width,
                    'height': height,
                    'duration': total_frames / fps
                }
            }
            
        finally:
            cap.release()
    
    def process_frame(self, frame: np.ndarray) -> Dict[str, Any]:
        """Process single frame for pose detection."""
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb_frame.flags.writeable = False
        
        # Run pose detection
        results = self.pose_detector.process(rgb_frame)
        
        if results.pose_landmarks:
            # Extract landmarks
            landmarks = []
            world_landmarks = []
            visibility_scores = []
            
            for landmark in results.pose_landmarks.landmark:
                landmarks.append({
                    'x': landmark.x,
                    'y': landmark.y,
                    'z': landmark.z,
                    'visibility': landmark.visibility
                })
                visibility_scores.append(landmark.visibility)
            
            if results.pose_world_landmarks:
                for landmark in results.pose_world_landmarks.landmark:
                    world_landmarks.append({
                        'x': landmark.x,
                        'y': landmark.y,
                        'z': landmark.z,
                        'visibility': landmark.visibility
                    })
            
            # Calculate overall confidence
            confidence = np.mean(visibility_scores)
            
            # Update motion buffer
            self._update_motion_buffer(landmarks)
            
            return {
                'landmarks': landmarks,
                'world_landmarks': world_landmarks,
                'confidence': confidence,
                'visibility_scores': visibility_scores,
                'has_pose': True
            }
        
        return {
            'landmarks': None,
            'world_landmarks': None,
            'confidence': 0,
            'visibility_scores': [],
            'has_pose': False
        }
    
    def draw_pose(self, frame: np.ndarray, landmarks) -> np.ndarray:
        """Draw pose landmarks on frame."""
        if landmarks:
            # Convert landmarks to MediaPipe format
            mp_landmarks = self.mp_pose.PoseLandmark
            
            # Draw the pose
            self.mp_drawing.draw_landmarks(
                frame,
                landmarks,
                self.mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style()
            )
        
        return frame
    
    def _update_motion_buffer(self, landmarks: List[Dict[str, float]]):
        """Update motion tracking buffer."""
        if landmarks:
            # Store key joint positions for motion analysis
            key_joints = {
                'left_wrist': landmarks[15] if len(landmarks) > 15 else None,
                'right_wrist': landmarks[16] if len(landmarks) > 16 else None,
                'left_hip': landmarks[23] if len(landmarks) > 23 else None,
                'right_hip': landmarks[24] if len(landmarks) > 24 else None,
                'nose': landmarks[0] if len(landmarks) > 0 else None
            }
            
            self.motion_buffer.append({
                'timestamp': time.time(),
                'joints': key_joints
            })
    
    def _calculate_motion_intensity(self) -> float:
        """Calculate current motion intensity from buffer."""
        if len(self.motion_buffer) < 2:
            return 0.0
        
        # Compare recent frames
        recent = self.motion_buffer[-1]
        previous = self.motion_buffer[-2]
        
        total_movement = 0
        joint_count = 0
        
        for joint_name in recent['joints']:
            if recent['joints'][joint_name] and previous['joints'][joint_name]:
                # Calculate Euclidean distance
                curr = recent['joints'][joint_name]
                prev = previous['joints'][joint_name]
                
                distance = np.sqrt(
                    (curr['x'] - prev['x'])**2 +
                    (curr['y'] - prev['y'])**2 +
                    (curr['z'] - prev['z'])**2
                )
                
                total_movement += distance
                joint_count += 1
        
        if joint_count > 0:
            return total_movement / joint_count
        return 0.0
    
    def _analyze_motion_patterns(self, poses: List[PoseFrame]) -> Dict[str, Any]:
        """Analyze motion patterns from pose sequence."""
        if not poses:
            return {}
        
        # Calculate movement velocities
        velocities = []
        accelerations = []
        
        for i in range(1, len(poses)):
            if poses[i].landmarks and poses[i-1].landmarks:
                # Calculate center of mass movement
                com_curr = self._calculate_center_of_mass(poses[i].landmarks)
                com_prev = self._calculate_center_of_mass(poses[i-1].landmarks)
                
                dt = poses[i].timestamp - poses[i-1].timestamp
                if dt > 0:
                    velocity = np.linalg.norm(np.array(com_curr) - np.array(com_prev)) / dt
                    velocities.append(velocity)
        
        # Calculate smoothness (lower variance = smoother)
        smoothness = 1.0 / (1.0 + np.var(velocities)) if velocities else 0
        
        # Detect pauses and transitions
        pauses = self._detect_pauses(velocities)
        
        return {
            'average_velocity': np.mean(velocities) if velocities else 0,
            'max_velocity': np.max(velocities) if velocities else 0,
            'smoothness_score': smoothness,
            'pause_count': len(pauses),
            'motion_consistency': self._calculate_consistency(poses)
        }
    
    def _calculate_center_of_mass(self, landmarks: List[Dict[str, float]]) -> tuple:
        """Calculate approximate center of mass from landmarks."""
        # Use torso landmarks for COM approximation
        torso_indices = [11, 12, 23, 24]  # shoulders and hips
        
        x_sum = sum(landmarks[i]['x'] for i in torso_indices if i < len(landmarks))
        y_sum = sum(landmarks[i]['y'] for i in torso_indices if i < len(landmarks))
        z_sum = sum(landmarks[i]['z'] for i in torso_indices if i < len(landmarks))
        
        count = len([i for i in torso_indices if i < len(landmarks)])
        
        if count > 0:
            return (x_sum / count, y_sum / count, z_sum / count)
        return (0, 0, 0)
    
    def _detect_pauses(self, velocities: List[float], threshold: float = 0.02) -> List[int]:
        """Detect pause points in motion."""
        pauses = []
        for i, vel in enumerate(velocities):
            if vel < threshold:
                pauses.append(i)
        return pauses
    
    def _calculate_consistency(self, poses: List[PoseFrame]) -> float:
        """Calculate motion consistency score."""
        if len(poses) < 2:
            return 0.0
        
        # Check consistency of detected landmarks
        detection_rates = []
        for pose in poses:
            if pose.landmarks:
                visible_count = sum(1 for l in pose.landmarks if l['visibility'] > 0.5)
                detection_rates.append(visible_count / len(pose.landmarks))
            else:
                detection_rates.append(0)
        
        return np.mean(detection_rates)
    
    def cleanup(self):
        """Clean up resources."""
        if self.pose_detector:
            self.pose_detector.close()