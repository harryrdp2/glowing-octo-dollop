# 🎬 DubSync Gradio Edition - Complete Guide

## 📖 Overview

यह Gradio version DubSync का है जो **Google Colab के लिए optimized** है।

### क्या है Special?

✅ **Automatic Public URLs** - Streamlit जैसी ngrok की जरूरत नहीं
✅ **Faster Setup** - Colab में आसानी से चलता है  
✅ **Better UI** - Modern, responsive interface
✅ **Share करना आसान** - Link share करो, दूसरे run कर सकते हैं
✅ **Offline capable** - Model download के बाद internet की जरूरत नहीं

---

## 🚀 Installation (Colab)

### Option 1: Quick Copy-Paste

```python
# एक ही cell में सब कुछ
!pip install -q gradio torch transformers librosa pydub moviepy demucs f5-tts yt-dlp ffmpeg-python
!apt-get install -y ffmpeg
!git clone https://github.com/harryrdp2/DubSync.git /content/DubSync
%cd /content/DubSync/DubSync
!python app_gradio.py
```

### Option 2: Step by Step

**Cell 1: Dependencies**
```python
!pip install -q --upgrade pip
!pip install -q gradio torch torchaudio transformers
!pip install -q librosa pydub moviepy demucs f5-tts
!pip install -q yt-dlp ffmpeg-python scipy numpy sentencepiece noisereduce
!apt-get update && apt-get install -y ffmpeg sox libsox-fmt-all
print("✅ Installation complete!")
```

**Cell 2: Clone & Setup**
```python
!git clone https://github.com/harryrdp2/DubSync.git /content/DubSync
%cd /content/DubSync/DubSync

import torch
print(f"✅ GPU Available: {torch.cuda.is_available()}")
print(f"✅ Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU'}")
```

**Cell 3: Run**
```python
!python app_gradio.py
```

---

## 🛠️ System Requirements

| Requirement | Minimum | Recommended |
|------------|---------|------------|
| **RAM** | 8 GB | 16 GB |
| **VRAM** | 4 GB | 12 GB (Colab GPU) |
| **Storage** | 5 GB | 10 GB |
| **Python** | 3.8+ | 3.10+ |
| **Colab Runtime** | CPU | GPU (free tier) or A100 |

---

## 🌍 Language Support

### Current Languages

**Input Languages (12+):**
```
Japanese (ja) - 🇯🇵
English (en) - 🇬🇧
Chinese (zh) - 🇨🇳
Korean (ko) - 🇰🇷
Spanish (es) - 🇪🇸
French (fr) - 🇫🇷
Hindi (hi) - 🇮🇳
German (de) - 🇩🇪
Italian (it) - 🇮🇹
Portuguese (pt) - 🇵🇹
Russian (ru) - 🇷🇺
Arabic (ar) - 🇸🇦
```

**Output Languages (3, expandable):**
```
English (en) - 🇬🇧
Chinese (zh) - 🇨🇳
Hindi (hi) - 🇮🇳
```

### Add More Languages

Edit `app_gradio.py`:

```python
target_lang = gr.Dropdown(
    label="🌍 Target Language",
    choices=["English", "Chinese", "Hindi", "French", "Spanish"],  # Add here
    value="English"
)
```

---

## 📊 Model Selection Guide

### Whisper Models

| Model | Size | Speed | Quality | VRAM | Best For |
|-------|------|-------|---------|------|----------|
| **tiny** | 39 MB | ⚡⚡⚡⚡⚡ | ⭐ | 1 GB | Quick tests |
| **base** | 140 MB | ⚡⚡⚡⚡ | ⭐⭐ | 2 GB | **Recommended** |
| **small** | 244 MB | ⚡⚡⚡ | ⭐⭐⭐ | 3 GB | Good balance |
| **medium** | 769 MB | ⚡⚡ | ⭐⭐⭐⭐ | 6 GB | Quality focused |
| **large** | 3 GB | ⚡ | ⭐⭐⭐⭐⭐ | 10 GB | Best quality |

**For Colab: `base` सबसे अच्छा है!**

---

## 🎯 Workflow

### Step-by-Step Process

```
1. Video URL → Download
         ↓
2. Extract Audio
         ↓
3. Separate Audio Layers (Demucs)
         ↓
4. Transcribe Vocals (Whisper)
         ↓
5. Translate Text (Helsinki-NLP)
         ↓
6. Clone Voices (F5-TTS)
         ↓
7. Mix Audio Layers
         ↓
8. Generate Final Video
         ↓
9. Create Subtitles (SRT)
         ↓
✅ Download Results
```

### Processing Times

```
Video Length: 2 minutes

Transcription: 5-15 min (model size पर depend)
Translation: 2-3 min
Voice Cloning: 5-15 min (segments पर depend)
Video Creation: 3-5 min
─────────────────────────
Total: 15-45 minutes

(First run: +10 min for model download)
```

---

## 🎨 UI Features

### Input Section
- 🎬 **Video URL** - YouTube या कोई भी video link
- 📍 **Source Language** - Original video की language
- 🌍 **Target Language** - Dubbed video की language
- 🎤 **Whisper Model** - Transcription quality vs speed

### Output Section
- 📋 **Status** - Real-time processing status
- 🎥 **Dubbed Video** - Final output video
- 📝 **Transcription Table** - Original + Translation

### Download Options
- Direct download buttons
- Subtitle file (.srt)
- CSV format transcription

---

## ⚙️ Configuration

### Default Settings

```python
# In app_gradio.py:

device = "cuda" if torch.cuda.is_available() else "cpu"
# Auto-selects GPU if available

temp_folder = "/tmp/dubsync_resources"
# Video processing folder

whisper_model = "base"  # Default model
# Change in dropdown
```

### Customize Settings

Edit `app_gradio.py`:

```python
# Change default model
whisper_model = gr.Dropdown(
    label="🎤 Whisper Model",
    choices=["tiny", "base", "small", "medium", "large"],
    value="small",  # Change default here
)

# Change output folder location
sample_output_dir = "/content/drive/MyDrive/DubSync"
# Works if using Google Drive
```

---

## 🔒 Privacy & Security

### Data Handling
```
Your Video ─────→ [Local Processing] ─────→ Your Device
        (Colab GPU)

✅ No external servers
✅ No data collection
✅ No API sharing
✅ Complete privacy
```

### Model Sources
- **Whisper**: OpenAI (open-source)
- **Opus-MT**: Helsinki-NLP (open-source)
- **F5-TTS**: Community (open-source)
- **Demucs**: Meta (open-source)

---

## 🐛 Troubleshooting

### Issue 1: "CUDA out of memory"

**Solution:**
```python
# Use smaller model
whisper_model = "base"  # instead of "large"

# Or restart kernel
!nvidia-smi  # Check memory
torch.cuda.empty_cache()  # Clear cache
```

### Issue 2: "ffmpeg command not found"

**Solution:**
```python
!apt-get update
!apt-get install -y ffmpeg
!which ffmpeg  # Verify
```

### Issue 3: "Model download failed"

**Solution:**
```python
# Check internet connection
# Try downloading manually
from transformers import MarianMTModel
model = MarianMTModel.from_pretrained("Helsinki-NLP/Opus-MT-ja-en")

# Wait a bit and retry
```

### Issue 4: "Processing is very slow"

**Solutions:**
1. Use smaller Whisper model (`base` instead of `medium`)
2. Use shorter video (2-3 minutes instead of 30 minutes)
3. Restart Colab (Runtime → Restart session)
4. Upgrade to Colab+ for A100 GPU

### Issue 5: "Gradio URL not appearing"

**Solution:**
```python
# Make sure Gradio is installed
!pip install --upgrade gradio

# Run with explicit settings
demo.launch(share=True, debug=True)
```

### Issue 6: "Video download failed"

**Solution:**
```python
# Check if it's a YouTube video
# Use direct video URL instead
# Check internet connection

# Try downloading manually first
!yt-dlp "your_video_url"
```

---

## 📈 Performance Optimization

### Speed Optimization

1. **Use GPU**
   ```python
   # Check if available
   import torch
   print(torch.cuda.is_available())
   ```

2. **Use smaller Whisper model**
   ```python
   choices=["tiny", "base"]  # Fast options
   ```

3. **Process shorter videos**
   ```python
   # 2-3 minutes videos are faster
   ```

4. **Batch processing**
   ```python
   # Process multiple videos sequentially
   ```

### Memory Optimization

```python
# Clear cache between runs
import gc
gc.collect()
torch.cuda.empty_cache()

# Use gradient checkpointing (if available)
model.gradient_checkpointing_enable()
```

---

## 📊 Comparison: Streamlit vs Gradio

### Gradio (Recommended for Colab)
✅ Automatic public URLs
✅ Lightweight
✅ Faster startup
✅ Better for Colab
✅ Mobile-friendly
✅ Live sharing
❌ Less customization

### Streamlit (Desktop focused)
✅ More customizable
✅ Richer components
✅ Better docs
❌ Needs ngrok
❌ Heavier
❌ Slower on Colab
❌ Complex sharing

---

## 🔄 Workflow Customization

### Modify Processing Steps

```python
# In app_gradio.py, you can:

# 1. Skip certain steps
if skip_audio_separation:
    pass  # Don't run Demucs

# 2. Change model paths
custom_whisper = "large-v2"
custom_lang_model = "some_other_model"

# 3. Adjust parameters
f5_tts_speed = 0.9  # Faster/slower

# 4. Add new features
# Any Python code can be added
```

---

## 🎓 Learning Resources

### Understand the Code

1. **Main Loop**: `process_video()` function
2. **Audio Processing**: `separate_audio_layers()`
3. **Translation**: `translate_segments()`
4. **Voice Cloning**: `voice_cloning()`
5. **UI**: Gradio blocks

### External Resources

- Gradio Docs: https://gradio.app/docs
- Whisper: https://github.com/openai/whisper
- Helsinki-NLP: https://huggingface.co/Helsinki-NLP
- F5-TTS: https://github.com/SWivid/F5-TTS

---

## 💾 Save Settings

### Google Drive Integration (Optional)

```python
from google.colab import drive
drive.mount('/content/drive')

# Output to Drive
output_path = '/content/drive/MyDrive/DubSync_Output'
os.makedirs(output_path, exist_ok=True)
```

### Create Config File

```python
import json

config = {
    "default_model": "base",
    "default_source": "en",
    "default_target": "hi",
    "output_dir": "/tmp/dubsync"
}

with open("config.json", "w") as f:
    json.dump(config, f)
```

---

## 🚀 Advanced Features

### Batch Processing

```python
videos = [
    "youtube.com/watch?v=...",
    "youtube.com/watch?v=...",
]

for video in videos:
    process_video(video, "en", "hi", "base")
```

### Custom Voice Profiles

```python
# Modify voice cloning parameters in app_gradio.py
f5_tts_params = {
    "speed": 0.8,
    "pitch": 1.0,  # (if supported)
}
```

### Export Formats

Currently exports:
- MP4 video + audio
- SRT subtitles
- CSV transcription

Can extend to:
- MKV with embedded subtitles
- VTT format subtitles
- JSON transcription

---

## 📋 Checklist

### Before Running
- [ ] GPU runtime selected
- [ ] ffmpeg installed
- [ ] Dependencies installed
- [ ] Video URL ready
- [ ] Target language selected

### During Processing
- [ ] Don't close browser
- [ ] Don't refresh Colab
- [ ] Monitor VRAM usage
- [ ] Check task progress

### After Completion
- [ ] Download video
- [ ] Download subtitles
- [ ] Download transcription
- [ ] Delete temp folders (optional)

---

## 📞 Support

### Common Issues

**Q: Public share link अभी भी काम क्यों नहीं कर रहा है?**
A: Colab session खत्म हो गया। फिर से चलाओ।

**Q: क्या मैं longer video process कर सकता हूँ?**
A: हाँ, lekin slowर होगा। Colab+ use करो।

**Q: किस browser को use करूँ?**
A: Chrome/Firefox recommended। Mobile भी चलेगा।

**Q: क्या offline काम करेगा?**
A: Model download के बाद हाँ!

---

## ✨ Summary

### Gradio Edition के फायदे:
- ✅ सबसे आसान Colab setup
- ✅ Automatic public URLs
- ✅ Super fast startup
- ✅ Mobile friendly
- ✅ Share करना आसान
- ✅ No configuration needed

### Perfect for:
- 🎓 Students
- 🎬 Content creators
- 🔬 Researchers
- 👥 Team collaboration
- 🌍 Global sharing

---

**Ready to dub? Just run `app_gradio.py` और enjoy! 🎉**

*"Gradio के साथ DubSync - Colab में सबसे आसान way!"*
