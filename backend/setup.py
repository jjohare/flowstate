#!/usr/bin/env python3
"""Setup script for Tai Chi Flow backend."""

import os
import sys
import subprocess
import platform
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("Error: Python 3.8 or higher is required")
        return False
    print(f"Python {version.major}.{version.minor}.{version.micro} detected")
    return True


def create_virtual_environment():
    """Create virtual environment if it doesn't exist."""
    venv_path = Path("venv")
    
    if venv_path.exists():
        print("Virtual environment already exists")
        return True
    
    print("Creating virtual environment...")
    try:
        subprocess.run([sys.executable, "-m", "venv", "venv"], check=True)
        print("Virtual environment created successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error creating virtual environment: {e}")
        return False


def get_pip_command():
    """Get the correct pip command for the platform."""
    if platform.system() == "Windows":
        return os.path.join("venv", "Scripts", "pip")
    else:
        return os.path.join("venv", "bin", "pip")


def install_dependencies():
    """Install Python dependencies."""
    pip_cmd = get_pip_command()
    
    print("Upgrading pip...")
    try:
        subprocess.run([pip_cmd, "install", "--upgrade", "pip"], check=True)
    except subprocess.CalledProcessError:
        print("Warning: Failed to upgrade pip")
    
    print("Installing dependencies from requirements.txt...")
    try:
        subprocess.run([pip_cmd, "install", "-r", "requirements.txt"], check=True)
        print("Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        return False


def test_imports():
    """Test that all required imports work."""
    print("\nTesting imports...")
    
    try:
        import flask
        print("✓ Flask imported successfully")
    except ImportError:
        print("✗ Failed to import Flask")
        return False
    
    try:
        import cv2
        print("✓ OpenCV imported successfully")
    except ImportError:
        print("✗ Failed to import OpenCV")
        return False
    
    try:
        import mediapipe
        print("✓ MediaPipe imported successfully")
    except ImportError:
        print("✗ Failed to import MediaPipe")
        return False
    
    try:
        import numpy
        print("✓ NumPy imported successfully")
    except ImportError:
        print("✗ Failed to import NumPy")
        return False
    
    return True


def create_directories():
    """Create necessary directories."""
    dirs = ["models", "logs", "temp"]
    
    for dir_name in dirs:
        dir_path = Path(dir_name)
        dir_path.mkdir(exist_ok=True)
        print(f"Created directory: {dir_name}")


def download_test_models():
    """Download test models if needed."""
    print("\nChecking models...")
    # MediaPipe downloads its models automatically
    print("MediaPipe will download models automatically on first use")
    
    # Create placeholder for custom models
    models_dir = Path("models")
    readme_path = models_dir / "README.md"
    
    if not readme_path.exists():
        readme_content = """# AI Models Directory

This directory contains AI models for Tai Chi motion analysis.

## Models:

1. **MediaPipe Pose Model** - Automatically downloaded by MediaPipe
2. **Custom Motion Analysis Models** - To be added in future versions

## Model Management:

Models are managed by the `model_manager.py` module.
"""
        with open(readme_path, "w") as f:
            f.write(readme_content)
        print("Created models README")


def main():
    """Run setup process."""
    print("Tai Chi Flow Backend Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return 1
    
    # Create virtual environment
    if not create_virtual_environment():
        return 1
    
    # Install dependencies
    if not install_dependencies():
        return 1
    
    # Create directories
    create_directories()
    
    # Download models
    download_test_models()
    
    # Test imports
    if not test_imports():
        print("\nSetup completed with errors. Please check the error messages above.")
        return 1
    
    print("\n" + "=" * 50)
    print("Setup completed successfully!")
    print("\nTo run the backend server:")
    
    if platform.system() == "Windows":
        print("  venv\\Scripts\\python app.py")
    else:
        print("  venv/bin/python app.py")
    
    print("\nOr activate the virtual environment first:")
    if platform.system() == "Windows":
        print("  venv\\Scripts\\activate")
    else:
        print("  source venv/bin/activate")
    print("  python app.py")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())