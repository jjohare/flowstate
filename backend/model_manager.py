"""Model manager for handling AI model downloading and initialization."""

import os
import json
import logging
import requests
import hashlib
from pathlib import Path
from typing import Dict, Any, Optional
import zipfile
import tarfile
from tqdm import tqdm

logger = logging.getLogger(__name__)


class ModelManager:
    """Manage AI models for pose detection and motion analysis."""
    
    def __init__(self, model_dir: Optional[str] = None):
        self.model_dir = Path(model_dir) if model_dir else Path.home() / '.taichi_models'
        self.model_dir.mkdir(parents=True, exist_ok=True)
        
        self.model_registry = {
            'pose': {
                'name': 'MediaPipe Pose Model',
                'type': 'mediapipe',
                'version': '2.3.0',
                'loaded': False,
                'auto_download': True  # MediaPipe handles its own models
            },
            'motion': {
                'name': 'Motion Analysis Model',
                'type': 'custom',
                'version': '1.0.0',
                'url': 'https://example.com/motion_model.zip',  # Placeholder
                'checksum': 'sha256:placeholder',
                'size_mb': 45,
                'loaded': False
            },
            'form_reference': {
                'name': 'Tai Chi Form References',
                'type': 'reference_data',
                'version': '1.0.0',
                'url': 'https://example.com/taichi_forms.json',  # Placeholder
                'loaded': False
            }
        }
        
        self.loaded_models = {}
        self.reference_data = {}
        
    def models_loaded(self) -> bool:
        """Check if all required models are loaded."""
        required_models = ['pose']  # Only pose is strictly required
        return all(self.model_registry.get(model, {}).get('loaded', False) for model in required_models)
    
    def is_model_loaded(self, model_name: str) -> bool:
        """Check if specific model is loaded."""
        return self.model_registry.get(model_name, {}).get('loaded', False)
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get information about all models."""
        info = {}
        for model_name, model_data in self.model_registry.items():
            info[model_name] = {
                'name': model_data['name'],
                'version': model_data['version'],
                'loaded': model_data['loaded'],
                'type': model_data['type']
            }
        return info
    
    def load_all_models(self):
        """Load all required models."""
        logger.info("Loading AI models...")
        
        # Load pose model (MediaPipe)
        self._load_pose_model()
        
        # Load reference data
        self._load_reference_data()
        
        # Load custom models if available
        self._load_custom_models()
        
        logger.info("Model loading complete")
    
    def _load_pose_model(self):
        """Load MediaPipe pose model."""
        try:
            # MediaPipe downloads its models automatically
            import mediapipe as mp
            
            # Test that MediaPipe is working
            mp_pose = mp.solutions.pose
            test_pose = mp_pose.Pose(static_image_mode=True)
            test_pose.close()
            
            self.model_registry['pose']['loaded'] = True
            logger.info("MediaPipe pose model loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load pose model: {e}")
            raise RuntimeError(f"Failed to initialize MediaPipe: {e}")
    
    def _load_reference_data(self):
        """Load Tai Chi form reference data."""
        reference_file = self.model_dir / 'taichi_forms.json'
        
        # Create default reference data if not exists
        if not reference_file.exists():
            default_forms = self._create_default_forms()
            with open(reference_file, 'w') as f:
                json.dump(default_forms, f, indent=2)
            logger.info("Created default Tai Chi form references")
        
        # Load reference data
        try:
            with open(reference_file, 'r') as f:
                self.reference_data = json.load(f)
            
            self.model_registry['form_reference']['loaded'] = True
            logger.info("Loaded Tai Chi form reference data")
            
        except Exception as e:
            logger.error(f"Failed to load reference data: {e}")
    
    def _load_custom_models(self):
        """Load custom motion analysis models if available."""
        # Placeholder for custom model loading
        # In production, this would load trained neural networks
        pass
    
    def download_model(self, model_name: str, progress_callback=None):
        """Download a specific model."""
        if model_name not in self.model_registry:
            raise ValueError(f"Unknown model: {model_name}")
        
        model_info = self.model_registry[model_name]
        
        if model_info.get('auto_download'):
            logger.info(f"Model {model_name} is auto-downloaded")
            return
        
        if 'url' not in model_info:
            logger.warning(f"No download URL for model {model_name}")
            return
        
        model_path = self.model_dir / f"{model_name}_v{model_info['version']}"
        
        if model_path.exists():
            logger.info(f"Model {model_name} already downloaded")
            return
        
        logger.info(f"Downloading model {model_name}...")
        
        try:
            response = requests.get(model_info['url'], stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            
            # Download with progress
            model_path.parent.mkdir(parents=True, exist_ok=True)
            temp_path = model_path.with_suffix('.tmp')
            
            with open(temp_path, 'wb') as f:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if progress_callback and total_size > 0:
                            progress = int((downloaded / total_size) * 100)
                            progress_callback(progress)
            
            # Verify checksum if provided
            if 'checksum' in model_info and model_info['checksum'] != 'placeholder':
                if not self._verify_checksum(temp_path, model_info['checksum']):
                    temp_path.unlink()
                    raise ValueError("Checksum verification failed")
            
            # Extract if compressed
            if model_info['url'].endswith('.zip'):
                self._extract_zip(temp_path, model_path)
                temp_path.unlink()
            elif model_info['url'].endswith('.tar.gz'):
                self._extract_tar(temp_path, model_path)
                temp_path.unlink()
            else:
                temp_path.rename(model_path)
            
            logger.info(f"Model {model_name} downloaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to download model {model_name}: {e}")
            raise
    
    def _verify_checksum(self, file_path: Path, expected_checksum: str) -> bool:
        """Verify file checksum."""
        algorithm, expected_hash = expected_checksum.split(':')
        
        if algorithm == 'sha256':
            hasher = hashlib.sha256()
        else:
            raise ValueError(f"Unsupported hash algorithm: {algorithm}")
        
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                hasher.update(chunk)
        
        actual_hash = hasher.hexdigest()
        return actual_hash == expected_hash
    
    def _extract_zip(self, zip_path: Path, extract_to: Path):
        """Extract zip file."""
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
    
    def _extract_tar(self, tar_path: Path, extract_to: Path):
        """Extract tar.gz file."""
        with tarfile.open(tar_path, 'r:gz') as tar_ref:
            tar_ref.extractall(extract_to)
    
    def _create_default_forms(self) -> Dict[str, Any]:
        """Create default Tai Chi form reference data."""
        return {
            'forms': {
                'yang_24': {
                    'name': 'Yang Style 24 Forms',
                    'movements': [
                        {
                            'id': 1,
                            'name': 'Commencing Form',
                            'duration_seconds': 5,
                            'key_points': [
                                'Stand naturally with feet together',
                                'Arms hang naturally at sides',
                                'Shift weight to right foot',
                                'Step left foot to shoulder width'
                            ]
                        },
                        {
                            'id': 2,
                            'name': 'Part Wild Horse\'s Mane',
                            'duration_seconds': 8,
                            'key_points': [
                                'Hold ball on right side',
                                'Step forward with left foot',
                                'Separate hands diagonally',
                                'Repeat on opposite side'
                            ]
                        },
                        # Additional movements would be defined here
                    ],
                    'total_duration_minutes': 5.5,
                    'difficulty': 'beginner',
                    'style': 'yang'
                },
                'yang_40': {
                    'name': 'Yang Style 40 Forms',
                    'movements': [],  # Would be populated with full movement list
                    'total_duration_minutes': 10,
                    'difficulty': 'intermediate',
                    'style': 'yang'
                },
                'chen_18': {
                    'name': 'Chen Style 18 Forms',
                    'movements': [],  # Would be populated with full movement list
                    'total_duration_minutes': 7,
                    'difficulty': 'intermediate',
                    'style': 'chen'
                }
            },
            'pose_quality_thresholds': {
                'excellent': 0.9,
                'good': 0.75,
                'fair': 0.6,
                'needs_improvement': 0.0
            },
            'key_principles': [
                'Relaxation and softness',
                'Continuous flowing movement',
                'Weight shifting and balance',
                'Coordination of upper and lower body',
                'Intent guides movement'
            ]
        }
    
    def get_form_reference(self, form_id: str) -> Optional[Dict[str, Any]]:
        """Get reference data for a specific form."""
        if not self.reference_data:
            return None
        
        return self.reference_data.get('forms', {}).get(form_id)
    
    def get_quality_thresholds(self) -> Dict[str, float]:
        """Get pose quality thresholds."""
        if not self.reference_data:
            return {
                'excellent': 0.9,
                'good': 0.75,
                'fair': 0.6,
                'needs_improvement': 0.0
            }
        
        return self.reference_data.get('pose_quality_thresholds', {})