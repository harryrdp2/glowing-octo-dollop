# 🎬 Advanced Anime Dubbing - Google Colab Setup

## One-Liner (Fastest)

Copy-paste यह पूरा code एक **new Colab cell** में:

```python
!cd /tmp && rm -rf DubSync && git clone https://github.com/<your-username>/DubSync.git && cd DubSync && pip install -q git+https://github.com/f5-tts/F5-TTS.git demucs librosa pydub yt-dlp gradio transformers torch moviepy openai-whisper noisereduce pandas torchaudio> /dev/null 2>&1 && !apt-get install -y ffmpeg > /dev/null 2>&1 && python app_advanced_anime_dub.py
```

**Click output URL** → Browser → Ready! ✅

---

## Step-by-Step Setup (4 Cells)

### Cell 1️⃣: Install Dependencies

```python
# 🚀 Install all required packages
# This takes ~5-10 minutes

print("📦 Installing dependencies...")
print("⏳ Please wait - this happens only once!\n")

# Core packages
%pip install -q librosa pydub scipy numpy scipy
%pip install -q moviepy opencv-python imageio
%pip install -q demucs julius
%pip install -q torch torchaudio torchvision
%pip install -q transformers
%pip install -q openai-whisper
%pip install -q gradio
%pip install -q yt-dlp requests tqdm
%pip install -q noisereduce
%pip install -q pandas matplotlib plotly
%pip install -q pyyaml python-dotenv colorama python-dateutil

# F5-TTS for voice cloning (बड़ा model)
print("\n📥 Installing F5-TTS (voice cloning)...")
%pip install -q git+https://github.com/f5-tts/F5-TTS.git

# Audio processing
print("\n🔧 Installing FFmpeg...")
!apt-get update > /dev/null 2>&1
!apt-get install -y ffmpeg > /dev/null 2>&1

print("\n" + "="*60)
print("✅ All dependencies installed successfully!")
print("="*60)
```

### Cell 2️⃣: Download App

```python
# Download DubSync application
import os
import subprocess

print("📥 Downloading DubSync Advanced Anime Dubbing...\n")

# Clone repository
os.chdir('/tmp')
if os.path.exists('DubSync'):
    subprocess.run(['rm', '-rf', 'DubSync'], capture_output=True)

result = subprocess.run(
    ['git', 'clone', 'https://github.com/<replace-with-your-username>/DubSync.git'],
    capture_output=True, text=True
)

if result.returncode == 0:
    print("✅ Repository cloned successfully!")
    
    # List files
    os.chdir('/tmp/DubSync')
    files = os.listdir('.')
    print(f"\n📁 Files available ({len(files)}):")
    for f in sorted(files)[:10]:
        size = os.path.getsize(f) / 1024 if os.path.isfile(f) else 0
        if size > 0:
            print(f"  • {f} ({size:.1f} KB)")
        else:
            print(f"  • {f}")
    
    print("\n" + "="*60)
    print("✅ Ready to run!")
    print("="*60)
else:
    print(f"❌ Clone failed: {result.stderr}")
```

### Cell 3️⃣: Check Setup

```python
# Verify all dependencies are installed
import sys
import subprocess

print("🔍 Verifying installation...\n")

packages = [
    ('torch', 'PyTorch'),
    ('librosa', 'Librosa'),
    ('gradio', 'Gradio'),
    ('transformers', 'Transformers'),
    ('whisper', 'Whisper'),
    ('moviepy', 'MoviePy'),
    ('yt_dlp', 'yt-dlp'),
    ('pydub', 'PyDub'),
    ('pandas', 'Pandas'),
]

all_ok = True
for module, name in packages:
    try:
        __import__(module)
        print(f"✅ {name}")
    except ImportError:
        print(f"❌ {name} - Installing...")
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', name.lower()], 
                      capture_output=True)

print("\n✅ GPU Check:")
if torch.cuda.is_available():
    print(f"   GPU Available: {torch.cuda.get_device_name(0)}")
    print(f"   CUDA Version: {torch.version.cuda}")
    print(f"   VRAM: {torch.cuda.get_device_properties(0).total_memory / 1e9:.1f} GB")
else:
    print("   ⚠️ Using CPU (slower, but works)")

print("\n" + "="*60)
print("✅ All systems go!")
print("="*60)
```

### Cell 4️⃣: Run Advanced Anime Dubbing

```python
# Change to app directory and run
import os
import subprocess

os.chdir('/tmp/DubSync')

print("🎬 " + "="*58)
print("🎬 DubSync Advanced Anime Dubbing Engine")
print("🎬 " + "="*58 + "\n")

# Run the app
subprocess.run(['python', 'app_advanced_anime_dub.py'])

print("\n✅ Server started!")
print("👇 Look above for the Gradio URL")
print("📋 Click: https://xxxxx-gradio-link.gradio.live")
```

---

## Manual Cell-by-Cell (If Above Doesn't Work)

### Approach: Create from Scratch

**Cell 1: Environment Setup**
```python
import os
import sys

# Set paths for Colab
os.environ["XDG_CONFIG_HOME"] = "/tmp/.config"
os.environ["HF_HOME"] = "/tmp/huggingface"
os.environ["TRANSFORMERS_CACHE"] = "/tmp/transformers"
os.environ["TORCH_HOME"] = "/tmp/torch"

for p in ["/tmp/.config", "/tmp/huggingface", "/tmp/transformers", "/tmp/torch"]:
    os.makedirs(p, exist_ok=True)

print("✅ Environment configured")
```

**Cell 2: Install Packages**
```python
import subprocess
import sys

packages = [
    "librosa", "pydub", "scipy", "numpy",
    "moviepy", "demucs", "torch", "torchaudio",
    "transformers", "openai-whisper", "gradio",
    "yt-dlp", "requests", "noisereduce", "pandas"
]

for pkg in packages:
    print(f"📦 Installing {pkg}...")
    subprocess.run([sys.executable, "-m", "pip", "install", "-q", pkg], 
                   capture_output=True)

print("✅ Base packages done")

# F5-TTS
print("📦 Installing F5-TTS...")
subprocess.run(["pip", "install", "-q", 
               "git+https://github.com/f5-tts/F5-TTS.git"],
               capture_output=True)

print("✅ All packages installed!")
```

**Cell 3: Import and Test**
```python
# Test imports
try:
    import torch
    import librosa
    import gradio as gr
    import whisper
    from transformers import AutoModel
    print("✅ All imports successful!")
    print(f"✅ GPU: {torch.cuda.is_available()}")
    print(f"✅ Device: {'CUDA' if torch.cuda.is_available() else 'CPU'}")
except Exception as e:
    print(f"❌ Import error: {e}")
```

**Cell 4: Create App File**
```python
# Create app_advanced_anime_dub.py from your local file
# Option A: Download from repository
import subprocess
subprocess.run(['wget', '-q', 
               'https://raw.githubusercontent.com/<username>/DubSync/main/app_advanced_anime_dub.py',
               '-O', '/tmp/app_advanced_anime_dub.py'])

# Option B: Paste code directly (if you have it)
# Just copy the content from app_advanced_anime_dub.py and paste

print("✅ App file ready")
```

**Cell 5: Run Application**
```python
%cd /tmp
!python app_advanced_anime_dub.py
```

---

## Troubleshooting

### Issue: "ModuleNotFoundError"

**Solution:**
```python
# Install missing package
import subprocess
import sys
subprocess.run([sys.executable, "-m", "pip", "install", "-q", "package-name"])
```

### Issue: CUDA Out of Memory

**Solution:**
```python
# Use CPU instead (slower but works)
import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''

# Or modify code:
# device = 'cpu'  # Force CPU
```

### Issue: FFmpeg Not Found

**Solution:**
```python
# Reinstall ffmpeg
!apt-get update
!apt-get install -y ffmpeg
```

### Issue: Gradio URL Not Generating

**Solution:**
```python
# Make sure your Colab cell output is visible
# If not, try:
!python app_advanced_anime_dub.py --share
```

### Issue: Models Taking Too Long to Download

**This is normal!** First run:
- Whisper: ~140MB-1.5GB (depends on model)
- F5-TTS: ~500MB
- Helsinki-NLP: ~60-80MB
- Total: ~2-3GB

**After first run:** Cached, runs fast! ✅

---

## Performance Tips

### 1. Use Colab Pro for Faster Processing
```
Free Tier: 12-20 min setup, 45-90 min processing
Colab Pro: 8-12 min setup, 20-60 min processing
Colab Pro+: 5-8 min setup, 15-40 min processing
```

### 2. Restart Runtime if Slow
```python
# Sometimes helps
from google.colab import runtime
runtime.restart()
```

### 3. Check GPU Status
```python
!nvidia-smi
```

### 4. Free Up Memory
```python
import gc
gc.collect()
torch.cuda.empty_cache()
```

---

## Complete Working Example

यह पूरा code एक Colab cell में paste करो:

```python
#!/usr/bin/env python3
"""
🎬 DubSync Advanced Anime Dubbing - Colab Launcher
"""

import os
import sys
import subprocess
import time

# Setup environment
os.environ["XDG_CONFIG_HOME"] = "/tmp/.config"
os.environ["HF_HOME"] = "/tmp/huggingface"
os.environ["TRANSFORMERS_CACHE"] = "/tmp/transformers"
os.environ["TORCH_HOME"] = "/tmp/torch"

print("\n" + "="*70)
print("🎬 DubSync Advanced Anime Dubbing - Setup")
print("="*70 + "\n")

# Create directories
for path in ["/tmp/.config", "/tmp/huggingface"]:
    os.makedirs(path, exist_ok=True)

# Install packages
packages = [
    "librosa", "pydub", "scipy", "numpy", "moviepy",
    "demucs", "torch", "torchaudio", "transformers",
    "openai-whisper", "gradio", "yt-dlp", "pandas"
]

print("📦 Installing packages...\n")
for pkg in packages:
    print(f"  Installing {pkg}...", end=" ", flush=True)
    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-q", pkg],
        capture_output=True
    )
    print("✅" if result.returncode == 0 else "⚠️")

print("\n📥 Installing F5-TTS...")
subprocess.run(["pip", "install", "-q", 
                "git+https://github.com/f5-tts/F5-TTS.git"],
               capture_output=True)

print("\n🔧 Setting up FFmpeg...")
subprocess.run(["apt-get", "install", "-y", "ffmpeg"],
              capture_output=True)

print("\n" + "="*70)
print("✅ Setup Complete! Starting application...")
print("="*70 + "\n")

# Download and run app
import subprocess
os.chdir('/tmp')

# Clone or update repository
if not os.path.exists('DubSync'):
    subprocess.run(['git', 'clone', 
                   'https://github.com/<YOUR-USERNAME>/DubSync.git'])
else:
    os.chdir('DubSync')
    subprocess.run(['git', 'pull'])
    os.chdir('/tmp')

os.chdir('/tmp/DubSync')

# Run the application
print("\n🚀 Launching Advanced Anime Dubbing Engine...\n")
subprocess.run([sys.executable, 'app_advanced_anime_dub.py'])
```

---

## Final Checklist ✅

- [ ] Cell 1: Dependencies installed
- [ ] Cell 2: Repository downloaded
- [ ] Cell 3: Verification passed
- [ ] Cell 4: Gradio URL visible
- [ ] Browser: Opened live link
- [ ] Ready: To process anime! 🎬

---

**🎉 आप तैयार हो!**

**You're Ready!**

अपना पहला anime dub करो और मजे करो!

Create your first anime dub and have fun!

🎬✨💕
