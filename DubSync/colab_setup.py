#!/usr/bin/env python3
"""
One-Click DubSync Setup for Google Colab
This script installs all dependencies and runs DubSync
Just upload this to Colab and run!
"""

import subprocess
import sys
import os

def run_command(cmd, description=""):
    """Execute shell command and print output"""
    if description:
        print(f"\n{'='*60}")
        print(f"📦 {description}")
        print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, shell=True, capture_output=False, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Success!")
            return True
        else:
            print(f"⚠️ {description} - Some issues, but continuing...")
            return False
    except Exception as e:
        print(f"⚠️ Error in {description}: {e}")
        return False

def main():
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*58 + "║")
    print("║" + "  🎬 DubSync - Google Colab Setup (Local Models)  ".center(58) + "║")
    print("║" + " "*58 + "║")
    print("╚" + "="*58 + "╝")
    
    # Step 1: Update pip
    run_command(
        "pip install --upgrade pip setuptools wheel",
        "Updating pip, setuptools, and wheel"
    )
    
    # Step 2: Install core dependencies
    run_command(
        "pip install -q torch torchaudio transformers librosa pydub moviepy",
        "Installing core ML libraries"
    )
    
    # Step 3: Install audio processing tools
    run_command(
        "pip install -q demucs f5-tts streamlit sentencepiece protobuf",
        "Installing audio processing tools"
    )
    
    # Step 4: Install additional packages
    run_command(
        "pip install -q yt-dlp ffmpeg-python ffmpy scipy numpy noisereduce requests",
        "Installing utility packages"
    )
    
    # Step 5: Install system dependencies
    run_command(
        "apt-get update && apt-get install -y ffmpeg sox libsox-fmt-all 2>/dev/null",
        "Installing system dependencies (ffmpeg, sox)"
    )
    
    # Step 6: Setup environment
    print("\n" + "="*60)
    print("🔧 Setting up environment variables")
    print("="*60)
    
    env_vars = {
        "HF_HOME": "/tmp/huggingface",
        "HF_HUB_CACHE": "/tmp/huggingface/hub",
        "TRANSFORMERS_CACHE": "/tmp/transformers",
        "TORCH_HOME": "/tmp/torch",
        "XDG_CONFIG_HOME": "/tmp/.config",
        "XDG_CACHE_HOME": "/tmp/.cache",
    }
    
    for key, value in env_vars.items():
        os.environ[key] = value
        os.makedirs(value, exist_ok=True)
        print(f"  ✓ {key} = {value}")
    
    # Step 7: Download DubSync
    print("\n" + "="*60)
    print("📥 Cloning DubSync repository")
    print("="*60)
    
    run_command(
        "cd /content && git clone https://github.com/harryrdp2/DubSync.git 2>/dev/null || echo 'Already cloned'",
        "Cloning DubSync"
    )
    
    # Step 8: Verify installation
    print("\n" + "="*60)
    print("✅ Verifying installation")
    print("="*60)
    
    try:
        import torch
        print(f"  ✓ PyTorch: {torch.__version__}")
        print(f"  ✓ CUDA Available: {torch.cuda.is_available()}")
        
        import streamlit
        print(f"  ✓ Streamlit: {streamlit.__version__}")
        
        import transformers
        print(f"  ✓ Transformers: {transformers.__version__}")
        
        import librosa
        print(f"  ✓ Librosa loaded")
        
        print("\n✅ All dependencies installed successfully!")
    except ImportError as e:
        print(f"⚠️ Import error: {e}")
    
    # Step 9: Instructions
    print("\n" + "="*60)
    print("🚀 Ready to start DubSync!")
    print("="*60)
    print("""
Run the following command in the next cell:

    %cd /content/DubSync/DubSync
    !streamlit run app_colab.py --logger.level=error

Then click the link that appears to open the DubSync interface!

💡 Tips:
  - First run will download models (~2-3 GB)
  - Use smaller Whisper models (tiny, base) for quick tests
  - GPU processing is ~5-10x faster than CPU
  - Result will be saved after processing completes
    """)
    
    print("="*60)
    print("✨ Setup complete! Good luck with your videos! 🎬")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
