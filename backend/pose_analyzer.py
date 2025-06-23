"""Pose analysis module for Tai Chi movement quality assessment."""

import numpy as np
from typing import List, Dict, Any, Optional, Tuple
import logging
from dataclasses import dataclass
from scipy.spatial.distance import cosine
from scipy.signal import savgol_filter
import math

logger = logging.getLogger(__name__)


@dataclass
class MovementQuality:
    """Quality metrics for a movement."""
    balance_score: float
    fluidity_score: float
    alignment_score: float
    timing_score: float
    overall_score: float
    feedback: List[str]


class PoseAnalyzer:
    """Analyze poses for Tai Chi form quality and correctness."""
    
    def __init__(self):
        # MediaPipe pose landmark indices
        self.POSE_LANDMARKS = {
            'nose': 0,
            'left_shoulder': 11,
            'right_shoulder': 12,
            'left_elbow': 13,
            'right_elbow': 14,
            'left_wrist': 15,
            'right_wrist': 16,
            'left_hip': 23,
            'right_hip': 24,
            'left_knee': 25,
            'right_knee': 26,
            'left_ankle': 27,
            'right_ankle': 28
        }
        
        # Tai Chi principles for evaluation
        self.principles = {
            'balance': {
                'weight': 0.3,
                'threshold': 0.02  # Maximum COM deviation
            },
            'fluidity': {
                'weight': 0.25,
                'threshold': 0.1  # Smoothness threshold
            },
            'alignment': {
                'weight': 0.25,
                'threshold': 15  # Degrees of acceptable misalignment
            },
            'timing': {
                'weight': 0.2,
                'threshold': 0.2  # Timing variance threshold
            }
        }
    
    def analyze_sequence(self, poses: List[Any]) -> Dict[str, Any]:
        """Analyze a sequence of poses for overall quality."""
        if not poses:
            return {'error': 'No poses to analyze'}
        
        # Extract valid poses with landmarks
        valid_poses = [p for p in poses if p.landmarks]
        
        if not valid_poses:
            return {'error': 'No valid poses detected'}
        
        logger.info(f"Analyzing sequence of {len(valid_poses)} poses")
        
        # Analyze different aspects
        balance_analysis = self._analyze_balance(valid_poses)
        fluidity_analysis = self._analyze_fluidity(valid_poses)
        alignment_analysis = self._analyze_alignment(valid_poses)
        timing_analysis = self._analyze_timing(valid_poses)
        
        # Calculate overall quality
        overall_score = (
            balance_analysis['score'] * self.principles['balance']['weight'] +
            fluidity_analysis['score'] * self.principles['fluidity']['weight'] +
            alignment_analysis['score'] * self.principles['alignment']['weight'] +
            timing_analysis['score'] * self.principles['timing']['weight']
        )
        
        # Generate feedback
        feedback = self._generate_feedback(
            balance_analysis,
            fluidity_analysis,
            alignment_analysis,
            timing_analysis
        )
        
        return {
            'overall_score': overall_score,
            'balance': balance_analysis,
            'fluidity': fluidity_analysis,
            'alignment': alignment_analysis,
            'timing': timing_analysis,
            'feedback': feedback,
            'quality_level': self._get_quality_level(overall_score)
        }
    
    def get_realtime_feedback(self, landmarks: List[Dict[str, float]]) -> Dict[str, Any]:
        """Get real-time feedback for current pose."""
        if not landmarks or len(landmarks) < 29:
            return {'error': 'Insufficient landmarks'}
        
        feedback = []
        warnings = []
        
        # Check balance
        com = self._calculate_center_of_mass_from_landmarks(landmarks)
        base_of_support = self._calculate_base_of_support(landmarks)
        
        if not self._is_balanced(com, base_of_support):
            warnings.append("Adjust your balance - center of mass is off")
        
        # Check key alignments
        spine_angle = self._calculate_spine_angle(landmarks)
        if abs(spine_angle - 90) > 15:  # Should be roughly vertical
            feedback.append("Keep your spine more upright")
        
        # Check arm positions
        arm_symmetry = self._check_arm_symmetry(landmarks)
        if arm_symmetry < 0.8:
            feedback.append("Focus on symmetrical arm movements")
        
        # Check stance width
        stance_width = self._calculate_stance_width(landmarks)
        if stance_width < 0.8 or stance_width > 1.5:  # Relative to shoulder width
            feedback.append("Adjust your stance width")
        
        return {
            'feedback': feedback,
            'warnings': warnings,
            'posture_score': self._calculate_posture_score(landmarks),
            'balance_indicator': self._is_balanced(com, base_of_support)
        }
    
    def compare_with_reference(self, user_poses: List[Any], reference_form: str) -> Dict[str, Any]:
        """Compare user performance with reference form."""
        # This would load reference data and compare
        # For now, return placeholder comparison
        
        if not user_poses:
            return {'error': 'No user poses to compare'}
        
        # Simulate comparison metrics
        comparison_scores = []
        frame_matches = []
        
        for i, pose in enumerate(user_poses):
            if pose.landmarks:
                # Calculate similarity score (placeholder)
                score = np.random.uniform(0.7, 0.95)
                comparison_scores.append(score)
                
                if score > 0.85:
                    frame_matches.append(i)
        
        avg_similarity = np.mean(comparison_scores) if comparison_scores else 0
        
        return {
            'average_similarity': avg_similarity,
            'best_match_frames': frame_matches[:10],  # Top 10 matches
            'improvement_areas': self._identify_improvement_areas(comparison_scores),
            'form_completion': len(frame_matches) / len(user_poses) if user_poses else 0
        }
    
    def _analyze_balance(self, poses: List[Any]) -> Dict[str, Any]:
        """Analyze balance throughout the sequence."""
        com_positions = []
        balance_scores = []
        
        for pose in poses:
            if pose.landmarks:
                com = self._calculate_center_of_mass_from_landmarks(pose.landmarks)
                base = self._calculate_base_of_support(pose.landmarks)
                
                com_positions.append(com)
                balance_scores.append(1.0 if self._is_balanced(com, base) else 0.5)
        
        # Calculate stability (low variance in COM)
        if com_positions:
            com_array = np.array(com_positions)
            stability = 1.0 - np.mean(np.std(com_array, axis=0))
            stability = max(0, min(1, stability))  # Clamp to [0, 1]
        else:
            stability = 0
        
        return {
            'score': np.mean(balance_scores) if balance_scores else 0,
            'stability': stability,
            'balance_maintained': sum(s == 1.0 for s in balance_scores),
            'total_frames': len(balance_scores)
        }
    
    def _analyze_fluidity(self, poses: List[Any]) -> Dict[str, Any]:
        """Analyze movement fluidity and smoothness."""
        if len(poses) < 3:
            return {'score': 0, 'smoothness': 0}
        
        # Track key joint trajectories
        joint_trajectories = {joint: [] for joint in ['left_wrist', 'right_wrist']}
        
        for pose in poses:
            if pose.landmarks and len(pose.landmarks) > 16:
                for joint, idx in [('left_wrist', 15), ('right_wrist', 16)]:
                    joint_trajectories[joint].append([
                        pose.landmarks[idx]['x'],
                        pose.landmarks[idx]['y'],
                        pose.landmarks[idx]['z']
                    ])
        
        # Calculate smoothness using jerk (third derivative)
        smoothness_scores = []
        
        for joint, trajectory in joint_trajectories.items():
            if len(trajectory) > 5:
                trajectory_array = np.array(trajectory)
                
                # Apply Savitzky-Golay filter for smoothing
                smoothed = savgol_filter(trajectory_array, 
                                       window_length=min(5, len(trajectory)),
                                       polyorder=2,
                                       axis=0)
                
                # Calculate jerk (simplified)
                velocities = np.diff(smoothed, axis=0)
                accelerations = np.diff(velocities, axis=0)
                jerks = np.diff(accelerations, axis=0)
                
                mean_jerk = np.mean(np.abs(jerks))
                smoothness = 1.0 / (1.0 + mean_jerk * 10)  # Normalize
                smoothness_scores.append(smoothness)
        
        return {
            'score': np.mean(smoothness_scores) if smoothness_scores else 0,
            'smoothness': np.mean(smoothness_scores) if smoothness_scores else 0,
            'continuous_flow': len(smoothness_scores) > 0
        }
    
    def _analyze_alignment(self, poses: List[Any]) -> Dict[str, Any]:
        """Analyze body alignment and posture."""
        alignment_scores = []
        posture_issues = []
        
        for pose in poses:
            if pose.landmarks and len(pose.landmarks) >= 29:
                # Check spine alignment
                spine_score = self._check_spine_alignment(pose.landmarks)
                
                # Check shoulder alignment
                shoulder_score = self._check_shoulder_alignment(pose.landmarks)
                
                # Check hip alignment
                hip_score = self._check_hip_alignment(pose.landmarks)
                
                # Combined alignment score
                alignment_score = np.mean([spine_score, shoulder_score, hip_score])
                alignment_scores.append(alignment_score)
                
                # Track issues
                if spine_score < 0.8:
                    posture_issues.append('spine')
                if shoulder_score < 0.8:
                    posture_issues.append('shoulders')
                if hip_score < 0.8:
                    posture_issues.append('hips')
        
        return {
            'score': np.mean(alignment_scores) if alignment_scores else 0,
            'average_alignment': np.mean(alignment_scores) if alignment_scores else 0,
            'common_issues': list(set(posture_issues))[:3]  # Top 3 issues
        }
    
    def _analyze_timing(self, poses: List[Any]) -> Dict[str, Any]:
        """Analyze movement timing and rhythm."""
        if len(poses) < 2:
            return {'score': 0, 'consistency': 0}
        
        # Calculate movement speeds between frames
        movement_speeds = []
        
        for i in range(1, len(poses)):
            if poses[i].landmarks and poses[i-1].landmarks:
                # Calculate average movement of key joints
                total_movement = 0
                joint_count = 0
                
                for joint_idx in [15, 16, 25, 26]:  # Wrists and knees
                    if joint_idx < len(poses[i].landmarks):
                        curr = poses[i].landmarks[joint_idx]
                        prev = poses[i-1].landmarks[joint_idx]
                        
                        movement = np.sqrt(
                            (curr['x'] - prev['x'])**2 +
                            (curr['y'] - prev['y'])**2 +
                            (curr['z'] - prev['z'])**2
                        )
                        
                        total_movement += movement
                        joint_count += 1
                
                if joint_count > 0:
                    avg_movement = total_movement / joint_count
                    time_diff = poses[i].timestamp - poses[i-1].timestamp
                    
                    if time_diff > 0:
                        speed = avg_movement / time_diff
                        movement_speeds.append(speed)
        
        # Analyze timing consistency
        if movement_speeds:
            speed_variance = np.var(movement_speeds)
            consistency = 1.0 / (1.0 + speed_variance * 10)  # Normalize
            
            # Check for appropriate pauses
            pause_quality = self._evaluate_pauses(movement_speeds)
            
            timing_score = (consistency + pause_quality) / 2
        else:
            timing_score = 0
            consistency = 0
        
        return {
            'score': timing_score,
            'consistency': consistency,
            'average_speed': np.mean(movement_speeds) if movement_speeds else 0,
            'speed_variation': np.std(movement_speeds) if movement_speeds else 0
        }
    
    def _calculate_center_of_mass_from_landmarks(self, landmarks: List[Dict[str, float]]) -> Tuple[float, float]:
        """Calculate 2D center of mass from landmarks."""
        # Use torso landmarks for COM approximation
        torso_indices = [11, 12, 23, 24]  # Shoulders and hips
        
        x_sum = 0
        y_sum = 0
        count = 0
        
        for idx in torso_indices:
            if idx < len(landmarks):
                x_sum += landmarks[idx]['x']
                y_sum += landmarks[idx]['y']
                count += 1
        
        if count > 0:
            return (x_sum / count, y_sum / count)
        return (0.5, 0.5)  # Default center
    
    def _calculate_base_of_support(self, landmarks: List[Dict[str, float]]) -> Tuple[float, float, float, float]:
        """Calculate base of support from ankle positions."""
        if len(landmarks) < 29:
            return (0.4, 0.8, 0.6, 0.9)  # Default base
        
        left_ankle = landmarks[27]
        right_ankle = landmarks[28]
        
        # Create bounding box around ankles
        min_x = min(left_ankle['x'], right_ankle['x']) - 0.05
        max_x = max(left_ankle['x'], right_ankle['x']) + 0.05
        min_y = min(left_ankle['y'], right_ankle['y']) - 0.05
        max_y = max(left_ankle['y'], right_ankle['y']) + 0.05
        
        return (min_x, min_y, max_x, max_y)
    
    def _is_balanced(self, com: Tuple[float, float], base: Tuple[float, float, float, float]) -> bool:
        """Check if center of mass is within base of support."""
        return (base[0] <= com[0] <= base[2] and base[1] <= com[1] <= base[3])
    
    def _calculate_spine_angle(self, landmarks: List[Dict[str, float]]) -> float:
        """Calculate spine angle from vertical."""
        if len(landmarks) < 25:
            return 90  # Default vertical
        
        # Use mid-shoulder to mid-hip
        mid_shoulder_x = (landmarks[11]['x'] + landmarks[12]['x']) / 2
        mid_shoulder_y = (landmarks[11]['y'] + landmarks[12]['y']) / 2
        
        mid_hip_x = (landmarks[23]['x'] + landmarks[24]['x']) / 2
        mid_hip_y = (landmarks[23]['y'] + landmarks[24]['y']) / 2
        
        # Calculate angle from vertical
        dx = mid_shoulder_x - mid_hip_x
        dy = mid_shoulder_y - mid_hip_y
        
        angle = math.degrees(math.atan2(dx, dy))
        return abs(angle)
    
    def _check_arm_symmetry(self, landmarks: List[Dict[str, float]]) -> float:
        """Check symmetry between left and right arms."""
        if len(landmarks) < 17:
            return 0
        
        # Compare arm positions relative to shoulders
        left_arm_vector = [
            landmarks[15]['x'] - landmarks[11]['x'],
            landmarks[15]['y'] - landmarks[11]['y'],
            landmarks[15]['z'] - landmarks[11]['z']
        ]
        
        right_arm_vector = [
            landmarks[16]['x'] - landmarks[12]['x'],
            landmarks[16]['y'] - landmarks[12]['y'],
            landmarks[16]['z'] - landmarks[12]['z']
        ]
        
        # Mirror right arm for comparison
        right_arm_vector[0] = -right_arm_vector[0]
        
        # Calculate cosine similarity
        similarity = 1 - cosine(left_arm_vector, right_arm_vector)
        return max(0, similarity)
    
    def _calculate_stance_width(self, landmarks: List[Dict[str, float]]) -> float:
        """Calculate stance width relative to shoulder width."""
        if len(landmarks) < 29:
            return 1.0
        
        shoulder_width = abs(landmarks[11]['x'] - landmarks[12]['x'])
        ankle_width = abs(landmarks[27]['x'] - landmarks[28]['x'])
        
        if shoulder_width > 0:
            return ankle_width / shoulder_width
        return 1.0
    
    def _calculate_posture_score(self, landmarks: List[Dict[str, float]]) -> float:
        """Calculate overall posture score."""
        scores = []
        
        # Spine alignment
        spine_angle = self._calculate_spine_angle(landmarks)
        spine_score = 1.0 - min(abs(spine_angle - 90) / 45, 1.0)
        scores.append(spine_score)
        
        # Shoulder level
        shoulder_level = abs(landmarks[11]['y'] - landmarks[12]['y'])
        shoulder_score = 1.0 - min(shoulder_level * 10, 1.0)
        scores.append(shoulder_score)
        
        # Hip level
        hip_level = abs(landmarks[23]['y'] - landmarks[24]['y'])
        hip_score = 1.0 - min(hip_level * 10, 1.0)
        scores.append(hip_score)
        
        return np.mean(scores)
    
    def _check_spine_alignment(self, landmarks: List[Dict[str, float]]) -> float:
        """Check spine alignment quality."""
        spine_angle = self._calculate_spine_angle(landmarks)
        
        # Ideal spine angle is close to 90 degrees (vertical)
        deviation = abs(spine_angle - 90)
        score = 1.0 - min(deviation / 45, 1.0)  # 45 degrees = score of 0
        
        return score
    
    def _check_shoulder_alignment(self, landmarks: List[Dict[str, float]]) -> float:
        """Check shoulder alignment and levelness."""
        if len(landmarks) < 13:
            return 0
        
        # Check if shoulders are level
        shoulder_diff = abs(landmarks[11]['y'] - landmarks[12]['y'])
        level_score = 1.0 - min(shoulder_diff * 10, 1.0)
        
        # Check if shoulders are relaxed (not raised)
        neck_shoulder_dist = abs(landmarks[11]['y'] - landmarks[0]['y'])
        relaxation_score = min(neck_shoulder_dist * 5, 1.0)
        
        return (level_score + relaxation_score) / 2
    
    def _check_hip_alignment(self, landmarks: List[Dict[str, float]]) -> float:
        """Check hip alignment and levelness."""
        if len(landmarks) < 25:
            return 0
        
        # Check if hips are level
        hip_diff = abs(landmarks[23]['y'] - landmarks[24]['y'])
        level_score = 1.0 - min(hip_diff * 10, 1.0)
        
        # Check hip-shoulder alignment
        hip_center_x = (landmarks[23]['x'] + landmarks[24]['x']) / 2
        shoulder_center_x = (landmarks[11]['x'] + landmarks[12]['x']) / 2
        
        alignment_diff = abs(hip_center_x - shoulder_center_x)
        alignment_score = 1.0 - min(alignment_diff * 10, 1.0)
        
        return (level_score + alignment_score) / 2
    
    def _evaluate_pauses(self, movement_speeds: List[float]) -> float:
        """Evaluate quality of movement pauses."""
        if not movement_speeds:
            return 0
        
        # Identify pauses (low movement speed)
        pause_threshold = np.percentile(movement_speeds, 20)
        pauses = [i for i, speed in enumerate(movement_speeds) if speed < pause_threshold]
        
        if not pauses:
            return 0.5  # No clear pauses
        
        # Check if pauses are well-distributed
        pause_distances = np.diff(pauses) if len(pauses) > 1 else []
        
        if pause_distances.size > 0:
            # Good pauses are evenly distributed
            distance_variance = np.var(pause_distances)
            distribution_score = 1.0 / (1.0 + distance_variance / 10)
            
            # Check pause duration consistency
            pause_durations = []
            for i in range(len(pauses) - 1):
                duration = pauses[i+1] - pauses[i]
                pause_durations.append(duration)
            
            if pause_durations:
                duration_variance = np.var(pause_durations)
                duration_score = 1.0 / (1.0 + duration_variance / 5)
                
                return (distribution_score + duration_score) / 2
        
        return 0.7  # Default score for single pause
    
    def _generate_feedback(self, balance: Dict, fluidity: Dict, alignment: Dict, timing: Dict) -> List[str]:
        """Generate actionable feedback based on analysis."""
        feedback = []
        
        # Balance feedback
        if balance['score'] < 0.7:
            feedback.append("Focus on maintaining better balance - keep your center of mass over your base of support")
        elif balance['stability'] < 0.6:
            feedback.append("Work on stability - minimize unnecessary swaying or shifting")
        
        # Fluidity feedback
        if fluidity['score'] < 0.7:
            feedback.append("Practice smoother transitions between movements - avoid sudden stops or jerky motions")
        
        # Alignment feedback
        if alignment['score'] < 0.7:
            common_issues = alignment.get('common_issues', [])
            if 'spine' in common_issues:
                feedback.append("Keep your spine more upright and aligned")
            if 'shoulders' in common_issues:
                feedback.append("Relax your shoulders and keep them level")
            if 'hips' in common_issues:
                feedback.append("Maintain proper hip alignment throughout the form")
        
        # Timing feedback
        if timing['score'] < 0.7:
            if timing['consistency'] < 0.6:
                feedback.append("Work on maintaining consistent speed throughout the form")
            else:
                feedback.append("Practice the rhythm and pacing of the movements")
        
        # Positive feedback
        scores = [balance['score'], fluidity['score'], alignment['score'], timing['score']]
        best_aspect = ['balance', 'fluidity', 'alignment', 'timing'][np.argmax(scores)]
        
        if max(scores) > 0.8:
            feedback.append(f"Excellent {best_aspect}! Keep up the good work")
        
        return feedback
    
    def _get_quality_level(self, score: float) -> str:
        """Get quality level description from score."""
        if score >= 0.9:
            return "Excellent"
        elif score >= 0.75:
            return "Good"
        elif score >= 0.6:
            return "Fair"
        else:
            return "Needs Improvement"
    
    def _identify_improvement_areas(self, scores: List[float]) -> List[str]:
        """Identify areas needing improvement from comparison scores."""
        if not scores:
            return []
        
        areas = []
        
        # Find segments with low scores
        low_score_threshold = 0.7
        low_segments = [i for i, score in enumerate(scores) if score < low_score_threshold]
        
        if len(low_segments) > len(scores) * 0.3:
            areas.append("Overall form accuracy needs improvement")
        elif low_segments:
            # Identify specific problem areas
            # Group consecutive low scores
            segment_groups = []
            current_group = [low_segments[0]]
            
            for i in range(1, len(low_segments)):
                if low_segments[i] - low_segments[i-1] <= 5:
                    current_group.append(low_segments[i])
                else:
                    segment_groups.append(current_group)
                    current_group = [low_segments[i]]
            
            if current_group:
                segment_groups.append(current_group)
            
            # Report major problem areas
            for group in segment_groups[:3]:  # Top 3 problem areas
                start_time = group[0] * 0.033  # Assuming 30 fps
                end_time = group[-1] * 0.033
                areas.append(f"Movement sequence from {start_time:.1f}s to {end_time:.1f}s")
        
        return areas