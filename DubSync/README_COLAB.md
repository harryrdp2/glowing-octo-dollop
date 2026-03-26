# 🎬 DubSync - Google Colab Setup Guide (No API Required)

## Overview
This guide walks you through running DubSync on Google Colab without any API keys. All models run locally on Colab's GPU.

---

## 🚀 Quick Start (Copy-Paste Commands)

### Step 1: Mount Google Drive (Optional - for saving outputs)
```python
from google.colab import drive
drive.mount('/content/drive')
```

### Step 2: Clone Repository
```bash
!cd /content && git clone https://github.com/harryrdp2/DubSync.git
%cd /content/DubSync/DubSync
```

### Step 3: Install Dependencies
```bash
!pip install --upgrade pip setuptools wheel
!pip install -r requirements_colab.txt
!apt-get update && apt-get install -y ffmpeg
```

### Step 4: Download Models (One-time, ~2-3 GB)
```python
import torch
print(f"GPU Available: {torch.cuda.is_available()}")

# Download Whisper model (choose one)
import whisper
model = whisper.load_model("base")  # or "small", "medium", "large"
print("✅ Whisper model downloaded")

# Download translation model
from transformers import MarianMTModel, MarianTokenizer
model_name = "Helsinki-NLP/Opus-MT-ja-en"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)
print("✅ Translation model downloaded")
```

### Step 5: Run Streamlit App
```bash
!streamlit run app_colab.py --logger.level=error --client.logger.level=error
```

After running, click the link to access the Streamlit interface.

---

## 📋 Detailed Installation Steps

### 1. Setup Colab Environment
```python
# Check GPU
!nvidia-smi

# Set up temp directories
import os
os.environ["HF_HOME"] = "/tmp/huggingface"
os.environ["TRANSFORMERS_CACHE"] = "/tmp/transformers"
os.environ["TORCH_HOME"] = "/tmp/torch"
```

### 2. Install System Dependencies
```bash
!apt-get update
!apt-get install -y ffmpeg sox libsox-fmt-all

# Install additional audio tools
!apt-get install -y libflac-dev libogg-dev libvorbis-dev
```

### 3. Install Python Packages
```bash
# Core packages
!pip install torch torchaudio transformers librosa

# Audio processing
!pip install pydub moviepy demucs

# Streamlit
!pip install streamlit

# Translation models
!pip install sentencepiece protobuf

# Optional: for better performance
!pip install noisereduce scipy numpy
```

---

## 🎯 Supported Languages

### Input Languages (Source):
- Japanese (ja)
- English (en)
- Chinese (zh)
- Korean (ko)
- Spanish (es)
- French (fr)
- German (de)
- Italian (it)
- Portuguese (pt)
- Russian (ru)
- Arabic (ar)
- Hindi (hi)

### Output Languages (Target):
- English (en)
- Chinese (zh)
- Hindi (hi)

To add more languages, the system uses Helsinki-NLP Opus-MT models. Supported pairs:
- Add to `output_languages` list in the code
- Model names: `Helsinki-NLP/Opus-MT-{source}-{target}`
- See: https://huggingface.co/Helsinki-NLP

---

## ⚙️ Model Selection & Performance

### Whisper Model Sizes (for transcription):

| Model | Size | Speed | Quality | RAM | VRAM |
|-------|------|-------|---------|-----|------|
| tiny | 39M | ⚡⚡⚡ | ⭐ | 1GB | 1GB |
| base | 140M | ⚡⚡ | ⭐⭐ | 1GB | 2GB |
| small | 244M | ⚡ | ⭐⭐⭐ | 2GB | 3GB |
| medium | 769M | - | ⭐⭐⭐⭐ | 5GB | 6GB |
| large | 3GB | ❌ | ⭐⭐⭐⭐⭐ | 10GB | 10GB |

**Recommendation for Colab**: 
- Quick tests: `tiny` or `base`
- Good quality: `small` or `medium`
- Best quality: `large` (need more resources)

---

## 🔧 Features & Capabilities

### ✅ What Works Locally (No API):
- ✨ **Transcription** - OpenAI Whisper (local download)
- 🌐 **Translation** - Helsinki-NLP Opus-MT (local download)
- 🎤 **Voice Cloning** - F5-TTS (local model)
- 🎵 **Audio Separation** - Demucs (local model)
- 🎬 **Video Processing** - MoviePy (local)
- 📊 **Subtitle Generation** - SRT format (local)

### ⚙️ No External APIs Required:
- ❌ NO OpenAI/Azure API keys needed
- ❌ NO payment required
- ❌ NO rate limits
- ❌ NO internet required after model download

---

## 📁 File Structure
```
DubSync/
├── app_colab.py           # Main Streamlit app (Colab version)
├── requirements_colab.txt # Colab dependencies
├── requirements.txt       # Original requirements
└── README_COLAB.md       # This file
```

---

## 🎬 Usage Workflow

1. **Upload/Link Video**: Enter YouTube URL or upload MP4
2. **Select Languages**: Choose source and target languages
3. **Choose Whisper Model**: Pick size based on quality & speed
4. **Configure Audio**: Enable/disable cleaning, set noise reduction
5. **Process**: Click to start (warning: can take 10-60 min depending on video length)
6. **Download**: Get dubbed video + transcription CSV

---

## 🐛 Troubleshooting

### Out of Memory Error
```python
# Clear cache
import torch
torch.cuda.empty_cache()

# Use smaller Whisper model (base instead of medium)
# Reduce video quality before processing
```

### Streamlit Connection Timeout
```bash
# Run with increased timeout
!streamlit run app_colab.py --client.toolbarMode=minimal --logger.level=error
```

### Translation Model Not Found
```python
# Pre-download model
from transformers import pipeline
pipe = pipeline("translation_ja_to_en", model="Helsinki-NLP/Opus-MT-ja-en")
print("✅ Model ready")
```

### CUDA Out of Memory
```python
# Set device priority
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

# Or use CPU for some operations
import torch
torch.cuda.empty_cache()
torch.cuda.reset_peak_memory_stats()
```

### ffmpeg Not Found
```bash
!apt-get install -y ffmpeg
!which ffmpeg
```

---

## 📊 Performance Expectations

### Processing Time (CPU/GPU):
- **Video Length**: 2 minutes
- **Total Time**: 15-45 minutes (GPU Colab)
- **Breakdown**:
  - Transcription: 5-15 min (depends on Whisper model)
  - Translation: 2-3 min
  - Voice Cloning: 5-15 min
  - Video Dubbing: 3-5 min

### GPU Requirements:
- **Minimum**: 12GB VRAM (Colab GPU)
- **Recommended**: 15GB+ VRAM (Colab A100)

---

## 🔑 Key Differences from Original

| Feature | Original | Colab Edition |
|---------|----------|---------------|
| Translation API | Azure OpenAI (GPT-4) | Helsinki-NLP Opus-MT |
| API Keys | ✅ Required | ❌ Not needed |
| Cost | Paid (API usage) | Free |
| Speed | Very fast (API) | Slower (local models) |
| Quality | Excellent | Good |
| Customization | Limited | Full control |

---

## 💡 Tips & Tricks

### Speed Optimization:
1. Use smaller Whisper model for quick tests
2. Enable audio cleaning (helps transcription)
3. Use 2-3 minute video clips instead of full videos
4. Restart Colab kernel between runs (clears cache)

### Quality Optimization:
1. Use largest available Whisper model (large-v3)
2. Pre-clean audio if possible
3. Choose appropriate source/target language pair
4. Use reference audio with clear speech

### Cost Optimization (Google Colab):
- Use free GPU tier (up to 12 hours daily)
- Upgrade to Colab+ for A100 (if needed)
- Keep session alive: refresh every 30 min
- Download results before session expires

---

## 🚀 Next Steps

1. **Try with sample video**: Test with short YouTube clip
2. **Experiment with models**: Try different Whisper sizes
3. **Add more languages**: Extend `output_languages` list
4. **Fine-tune voice**: Adjust F5-TTS parameters

---

## 📚 References

- **Streamlit**: https://streamlit.io/
- **OpenAI Whisper**: https://github.com/openai/whisper
- **Helsinki-NLP**: https://huggingface.co/Helsinki-NLP
- **F5-TTS**: https://github.com/SWivid/F5-TTS
- **Demucs**: https://github.com/facebookresearch/demucs

---

## ⚡ Quick Colab Command

Copy-paste this entire block into a Colab cell:

```python
# Install & Setup
!pip install -q torch torchaudio transformers librosa pydub moviepy demucs streamlit sentencepiece protobuf noisereduce scipy numpy

# Install system dependencies
!apt-get update && apt-get install -y ffmpeg sox libsox-fmt-all

# Clone and run
!cd /content && git clone https://github.com/harryrdp2/DubSync.git
%cd /content/DubSync/DubSync
!streamlit run app_colab.py --logger.level=error 2>/dev/null

print("\n✅ Streamlit is running! Click the link above.")
```

---

## ❓ FAQ

**Q: Do I need an API key?**  
A: No! All models run locally on your Colab GPU.

**Q: How long does processing take?**  
A: 15-45 minutes for a 2-minute video (depends on Whisper model).

**Q: What video formats are supported?**  
A: MP4, MKV, AVI, WebM (via YouTube links).

**Q: Can I use CPU only?**  
A: Yes, but it will be 5-10x slower. Recommended to use GPU.

**Q: How much storage/RAM is needed?**  
A: ~3-5GB for models, ~5-10GB for processing.

**Q: Can I translate to more languages?**  
A: Yes! Add language pairs to the code (see Helsinki-NLP models).

---

## 📧 Support

For issues or questions:
1. Check Troubleshooting section above
2. Review Streamlit/library documentation
3. Check Colab resource limits (GPU availability)
4. Restart kernel and try again

---

**Happy Dubbing! 🎬✨**
