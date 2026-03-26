# Google Colab One-Click Setup for DubSync Gradio

यह notebook एक full-featured Colab notebook के लिए है।

नीचे दिया गया code सीधे Google Colab में copy-paste करो!

---

## 🎬 DubSync Gradio - Colab Notebook

### Cell 1: Install All Dependencies

```python
print("🚀 DubSync Gradio - Google Colab Setup\n")

# Install main packages
print("📦 Installing packages...\n")
!pip install -q gradio
!pip install -q torch torchaudio
!pip install -q transformers librosa
!pip install -q pydub moviepy demucs f5-tts
!pip install -q yt-dlp ffmpeg-python scipy numpy
!pip install -q sentencepiece protobuf noisereduce pandas requests

# Install system dependencies
print("\n📦 Installing system tools...\n")
!apt-get update -qq > /dev/null 2>&1
!apt-get install -y ffmpeg sox libsox-fmt-all > /dev/null 2>&1

print("✅ All packages installed!")
```

### Cell 2: Clone DubSync

```python
print("📥 Cloning DubSync repository...\n")

!cd /content && git clone https://github.com/harryrdp2/DubSync.git 2>/dev/null || echo "Repository already exists"

# List files to verify
!ls -la /content/DubSync/DubSync/app_gradio.py

print("\n✅ DubSync cloned successfully!")
```

### Cell 3: Verify Setup & Download Models

```python
print("🔍 Verifying installation...\n")

import torch
import sys

print(f"✅ Python: {sys.version.split()[0]}")
print(f"✅ PyTorch: {torch.__version__}")
print(f"✅ CUDA Available: {torch.cuda.is_available()}")

if torch.cuda.is_available():
    print(f"✅ GPU: {torch.cuda.get_device_name(0)}")
    print(f"✅ CUDA: {torch.version.cuda}")
else:
    print("⚠️ CPU mode - Processing will be slower")

# Preload Whisper model
print("\n📥 Preloading Whisper model (one-time download ~150MB)...\n")
import whisper

try:
    model = whisper.load_model("base", device="cuda" if torch.cuda.is_available() else "cpu")
    print("✅ Whisper model loaded!")
except Exception as e:
    print(f"⚠️ Warning: {e}")
    print("You can still run DubSync, it will download the model automatically")

print("\n" + "="*60)
print("✨ Setup Complete! Ready to run DubSync!")
print("="*60)
```

### Cell 4: Run DubSync Gradio

```python
print("\n🎬 Starting DubSync Gradio...\n")

import os
import sys

os.chdir('/content/DubSync/DubSync')

# Run the app
exec(open('app_gradio.py').read())

# OR if you prefer subprocess:
# import subprocess
# subprocess.run(['python', 'app_gradio.py'])
```

---

## ⚡ Quick One-Liner Version

अगर सिर्फ एक cell में सब कुछ चलाना है:

```python
!pip install -q gradio torch transformers librosa pydub moviepy demucs f5-tts yt-dlp ffmpeg-python scipy numpy sentencepiece >= /dev/null 2>&1 && \
!apt-get install -y ffmpeg sox > /dev/null 2>&1 && \
!git clone https://github.com/harryrdp2/DubSync.git /content/DubSync 2>/dev/null && \
cd /content/DubSync/DubSync && \
python app_gradio.py
```

---

## 🎯 Usage Tips

### 1️⃣ First Time Setup (5-10 minutes)
- Run Cell 1: Install dependencies
- Run Cell 2: Clone repo
- Run Cell 3: Verify setup

### 2️⃣ Run DubSync
- Run Cell 4: Start Gradio
- Click the public link
- Paste video URL
- Click "🚀 Process Video"

### 3️⃣ Download Results
- Click download buttons
- Or save to Google Drive

---

## 📌 Important Notes

### ⏱️ Processing Time
- **First run**: ~15-20 min (model download + processing)
- **Subsequent runs**: ~15-45 min per video

### 💾 Storage
- Models: ~2-3 GB
- Processing temp files: ~5-10 GB
- Keep at least 15 GB free space

### 🖥️ GPU Settings
Go to: **Runtime → Change runtime type → GPU (free or A100 if Colab+)**

### 🔗 Sharing
Gradio creates public URL automatically! Share with others!

---

## 🐛 Troubleshooting

### If GPU is not available
```python
# Check devices
import torch
print(torch.cuda.is_available())
print(torch.cuda.device_count())

# Restart runtime and select GPU
# Runtime → Restart session → Change runtime type → GPU
```

### If ffmpeg is missing
```python
!apt-get update -qq
!apt-get install -y ffmpeg
!which ffmpeg
```

### If out of memory
```python
# Restart Colab
# Use smaller Whisper model (tiny or base)
# Process shorter videos
```

### If stuck processing
```python
# Interrupt kernel: Ctrl+M I (or stop button)
# Restart and try again
# Use smaller model
```

---

## 💡 Pro Tips

1. **Test with short videos first** (30 sec - 1 min)
2. **Use `base` Whisper model** for balance of speed/quality
3. **Close other tabs** to save Colab resources
4. **Don't refresh page** during processing
5. **Download results immediately** after processing

---

## 🌍 Supported Languages

**Input**: Japanese, English, Chinese, Korean, Spanish, French, Hindi, German, Italian, Portuguese, Russian, Arabic

**Output**: English, Chinese, Hindi

---

## 📚 More Information

- **Quick Start**: `GRADIO_QUICK_START.md`
- **Full Guide**: `GRADIO_GUIDE.md`
- **Other versions**: `app_colab.py` (Streamlit), `app.py` (original)

---

## ❓ FAQ

**Q: Kya internet connection zaroori hai?**
A: Model download ke liye haan. Baaki sab local hai.

**Q: Kitna time lagega?**
A: 15-45 minutes video length ke hisaab se.

**Q: Kya multilingual support hai?**
A: Haan! 100+ language pairs available hain.

**Q: Kya privacy safe hai?**
A: Bilkul! Sab kuch local process hota hai. Sab data aapke paas rehta hai.

**Q: Kya mein results share kar sakta hu?**
A: Gradio URL hi bata do! Dusre log directly use kar sakte hain.

---

## 🎉 Ready to Go!

```
1️⃣ Run Cell 1
   ↓
2️⃣ Run Cell 2
   ↓
3️⃣ Run Cell 3
   ↓
4️⃣ Run Cell 4
   ↓
🎬 Click link
   ↓
✨ Dub your videos!
```

---

**Any questions? Check the documentation files!**

- `GRADIO_QUICK_START.md` - 5 minute guide
- `GRADIO_GUIDE.md` - Complete reference
- `README_COLAB.md` - Original Streamlit guide

**अब शुरू करो! Happy Dubbing! 🎉**
