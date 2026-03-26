# 🚨 Advanced Anime Dubbing - Complete Troubleshooting Guide

## Common Issues & Solutions

---

## 🎵 Audio Quality Issues

### Problem: Dubbed Audio Sounds Robotic

**Symptoms:**
- Voice sounds artificial/mechanical
- Emotion not present
- Sounds like text-to-speech (TTS)

**Cause:**
- Speech speed too high
- Emotion parameters not applied
- Poor reference audio

**Solutions:**

```python
# ✅ Solution 1: Reduce Speech Speed
# In the code, change:
speed = 0.8  # Original (clear)
speed = 0.7  # Try this (more natural)

# The slower the speed, the less robotic it sounds
```

```python
# ✅ Solution 2: Increase Reference Audio Quality
# Use longer reference (5+ seconds instead of 1-2)
# This gives F5-TTS better voice pattern to learn

# In code:
start_ms = int(segment["start"] * 1000)
end_ms = int(segment["end"] * 1000)
# Make this duration longer:
end_ms = min(end_ms, start_ms + 5000)  # Max 5 seconds
```

```python
# ✅ Solution 3: Use Better Whisper Model
# tiny, base → small or medium
whisper_model = "small"  # More accurate transcription = better output
```

### Problem: Audio Too Quiet or Too Loud

**Symptoms:**
- Volume inconsistent between characters
- Need to increase volume significantly
- Or volume is distorted

**Cause:**
- Energy adjustment too low/high
- Original volume mix problem

**Solutions:**

```python
# ✅ Fix Energy Levels
# In emotion adjustment section:

emotion_params = {
    "angry": {"energy": 1.4},   # Increase to 1.5-1.6 if too quiet
    "happy": {"energy": 1.2},   # Increase to 1.3-1.4
    "sad": {"energy": 0.7},     # Keep soft
}

# Also normalize final audio:
max_val = np.max(np.abs(y_energy))
y_energy = y_energy / max_val * 0.95  # Prevent clipping
```

### Problem: Echo or Reverb in Dubbed Audio

**Symptoms:**
- Sound like it's in a cave
- Eco/reverb effect
- Unnatural tail on words

**Cause:**
- Audio separation (Demucs) not clean
- Original background retention

**Solutions:**

```python
# ✅ Use Better Audio Separation
# Replace demucs with:
!demucs --device=cuda -n=htdemucs_ft audio.wav
# Use the "_ft" (fine-tuned) model for better separation

# Or manually adjust:
"vocals": os.path.join(separated_dir, "vocals.wav"),
# Use ONLY vocal track, discard others for dubbed version
```

---

## 🎭 Character & Voice Issues

### Problem: Character Voice Not Recognized

**Symptoms:**
- "Character character_1 not found"
- Voice cloning skipped for some characters
- Wrong character gets wrong voice

**Cause:**
- Character names don't match
- JSON format wrong
- Speaker detection failed

**Solutions:**

```python
# ✅ Solution 1: Check Character Names Match

# In original anime:
Narrator: "Taro has arrived"
Character JSON must use EXACT names:
{
    "taro": {"name": "Taro"},        # ✅ Correct
    "Taro": {"name": "Taro"},        # Also works
    "t-aro": {"name": "Taro"},       # ❌ Won't match
}

# ✅ Solution 2: Verify JSON Format
import json
characters_json = '{"taro": {"name": "Taro"}}'
try:
    data = json.loads(characters_json)
    print("✅ Valid JSON")
except json.JSONDecodeError as e:
    print(f"❌ JSON Error: {e}")

# ✅ Solution 3: Use Speaker Diarization
# In transcription, add speaker detection:
result = model.transcribe(
    audio_path,
    language="ja",
    word_timestamps=True,
    # Add for speaker identification:
)
```

### Problem: All Characters Sound Exactly Alike

**Symptoms:**
- No character differentiation
- All voiced by same actor
- No personality difference

**Cause:**
- F5-TTS using same reference for all
- No voice adjustments per character
- Poor character detection

**Solutions:**

```python
# ✅ Solution 1: Per-Character Voice Adjustments
character_profiles = {
    "taro": {
        "pitch": 1.1,      # Slightly higher for young male
        "speed": 0.85,     # Normal speaking speed
        "energy": 1.0      # Normal volume
    },
    "yuki": {
        "pitch": 1.2,      # Higher for female
        "speed": 0.9,      # Slightly faster
        "energy": 0.95     # Slightly quieter
    },
    "villain": {
        "pitch": 0.8,      # Lower for older male
        "speed": 0.75,     # Slower, deliberate
        "energy": 1.2      # Powerful voice
    }
}

# ✅ Solution 2: Use Different F5-TTS Parameters
# For each character, use unique reference:
for char_id, segment in segments:
    char_profile = character_profiles.get(char_id)
    
    # Use character's unique voice sample
    ref_audio = char_profile.get("voice_sample")
    
    # Generate with adjustment
    pitch_shift = char_profile.get("pitch", 1.0)
    
    output = f5tts_infer(
        ref_audio=ref_audio,
        ref_text=original_text,
        gen_text=translated_text,
        speed=char_profile.get("speed", 0.8)
    )
    
    # Apply pitch
    output = librosa.effects.pitch_shift(
        output, sr=16000, 
        n_steps=pitch_shift * 2 - 2
    )
```

### Problem: Voice Cloning Failed for Some Characters

**Symptoms:**
- "Segment X cloning failed"
- Some characters missing voices
- Output audio missing sections

**Cause:**
- F5-TTS model timeout
- Reference audio too short
- Model loading issue

**Solutions:**

```python
# ✅ Solution 1: Increase Timeout
# In voice cloning loop:
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("F5-TTS took too long")

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(300)  # 5-minute timeout

try:
    # Run F5-TTS
    result = subprocess.run(command, capture_output=True, timeout=300)
except TimeoutError:
    print(f"⚠️ Segment {idx} timeout, using original audio")

# ✅ Solution 2: Use Fallback
try:
    # Try advanced cloning
    output = advanced_clone()
except:
    # Fallback to basic TTS
    output = basic_tts(translated_text)
    print(f"⚠️ Using fallback for segment {idx}")

# ✅ Solution 3: Reduce Model Size
# Use smaller reference audio:
# Instead of: 5-10 seconds
# Use: 2-3 seconds
```

---

## 📊 Lip-Sync Issues

### Problem: Lips Not Synchronized with Words

**Symptoms:**
- Mouth moves before/after words
- Mis-timed lip movements
- Looks dubbed (bad)

**Cause:**
- Segment timing wrong
- Dubbed audio duration mismatch
- Frame synchronization error

**Solutions:**

```python
# ✅ Solution 1: Fix Segment Duration Matching
for segment in segments:
    start_ms = int(segment["start"] * 1000)
    end_ms = int(segment["end"] * 1000)
    target_duration = end_ms - start_ms
    
    # Load cloned audio
    cloned = AudioSegment.from_file(cloned_path)
    cloned_duration = len(cloned)
    
    # Exact matching with time-stretching
    if cloned_duration != target_duration:
        stretch_ratio = target_duration / cloned_duration
        
        # Use sox for better stretching
        os.system(f"""
            sox {cloned_path} {output_path} tempo {stretch_ratio}
        """)

# ✅ Solution 2: Use Finer Segment Boundaries
# Instead of whole sentence, use smaller chunks:
# Before: "Naruto: Yosh! Ganbatte! Let's go!"
# After: 
#   Segment 1: "Yosh!"
#   Segment 2: "Ganbatte!"
#   Segment 3: "Let's go!"

# Better lip-sync granularity

# ✅ Solution 3: Manual Sync Adjustment
# After dubbing, manually adjust timing:
segment["start"] += 0.1  # Shift forward 100ms if needed
segment["end"] -= 0.05   # Trim if needed
```

---

## ⚙️ Processing & Technical Issues

### Problem: "CUDA Out of Memory"

**Symptoms:**
```
RuntimeError: CUDA out of memory. Tried to allocate 2.00 GiB
```

**Cause:**
- Video too long
- Model too large for GPU
- Multiple models loaded

**Solutions:**

```python
# ✅ Solution 1: Use CPU Instead
import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''
device = 'cpu'  # Force CPU

# Slower but works. Runtime: 2-3x longer

# ✅ Solution 2: Reduce Model Size
whisper_model = "tiny"     # Smallest (~75MB)
whisper_model = "base"     # Small (~140MB)
whisper_model = "small"    # Not recommended

# ✅ Solution 3: Process Shorter Videos
# First test: <2 minutes
# Then: <5 minutes
# Then: Longer if works

# ✅ Solution 4: Clear Memory Between Segments
import gc
for segment in segments:
    # Process one segment
    # ...
    gc.collect()
    torch.cuda.empty_cache()

# ✅ Solution 5: Use Colab Pro
# Better GPU (V100/A100 instead of T4)
# Higher memory limit
```

### Problem: "Model Download Timeout"

**Symptoms:**
```
ConnectionError: Connection timeout
URLError: urlopen error timed out
```

**Cause:**
- Slow internet
- Model server slow
- Network interruption

**Solutions:**

```python
# ✅ Solution 1: Manual Model Download
import torch
from transformers import AutoTokenizer, AutoModel

# Download explicitly
tokenizer = AutoTokenizer.from_pretrained(
    "Helsinki-NLP/Opus-MT-ja-hi",
    cache_dir="/tmp/transformers"
)

model = AutoModel.from_pretrained(
    "Helsinki-NLP/Opus-MT-ja-hi",
    cache_dir="/tmp/transformers"
)
# This downloads with retry logic

# ✅ Solution 2: Use Offline Mode
os.environ['HF_DATASETS_OFFLINE'] = '1'
os.environ['TRANSFORMERS_OFFLINE'] = '1'

# ✅ Solution 3: Retry Logic
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=2, min=4, max=10)
)
def download_model(model_name):
    return AutoModel.from_pretrained(model_name)

model = download_model("Helsinki-NLP/Opus-MT-ja-hi")
```

### Problem: "FFmpeg Not Found"

**Symptoms:**
```
FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'
```

**Cause:**
- FFmpeg not installed
- Not in PATH

**Solutions:**

```python
# ✅ Solution 1: Install FFmpeg (Colab)
!apt-get update
!apt-get install -y ffmpeg

# Verify:
!which ffmpeg
!ffmpeg -version

# ✅ Solution 2: Install with Conda
!conda install -c conda-forge ffmpeg

# ✅ Solution 3: Use Alternative
# Instead of FFmpeg-dependent code:
from PIL import Image
import av  # PyAV alternative
```

### Problem: "Video Processing Takes Forever"

**Symptoms:**
- Started 30 minutes ago, still "Mixing dubbed audio..."
- Processing stuck on one frame
- Very slow frame-by-frame encoding

**Cause:**
- Video resolution too high
- Hardware not optimal
- Memory pressure

**Solutions:**

```python
# ✅ Solution 1: Reduce Output Quality
# In MoviePy video writing:
video_with_audio.write_videofile(
    output_path,
    codec="libx264",
    preset="fast",  # faster encoding (medium/fast/faster)
    fps=24,         # reduce from 30
    verbose=False
)

# ✅ Solution 2: Reduce Video Resolution
video_resized = video.resize(width=720)  # Instead of 1080
video_resized.write_videofile(output_path)

# ✅ Solution 3: Check CPU Usage
import psutil
cpu_percent = psutil.cpu_percent(interval=1)
ram_percent = psutil.virtual_memory().percent
print(f"CPU: {cpu_percent}%, RAM: {ram_percent}%")

# If high CPU but no progress, something is stuck

# ✅ Solution 4: Use Colab Pro
# Better hardware = faster rendering
```

---

## 🌐 Translation Issues

### Problem: Translation Quality Poor

**Symptoms:**
- Translation sounds weird
- Grammar wrong
- Words don't match
- Meaning changed

**Cause:**
- Model limitation
- Text too long for model
- Language pair not well-supported

**Solutions:**

```python
# ✅ Solution 1: Break Long Text
# Instead of: "This is a very long sentence that goes on and on"
# Use: ["This is a long sentence", "that goes on", "and on"]

segments_to_translate = [
    seg[:50] for seg in long_segments  # Max 50 chars each
]

# ✅ Solution 2: Use Better Translation Model
# Instead of: Opus-MT
# Try: mBART, FLAN-T5, etc.

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

model_name = "google/mt5-base"  # Better for low-resource
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

# ✅ Solution 3: Post-Process Translation
def fix_translation(text, target_lang):
    # Manual corrections dictionary
    corrections = {
        "ja": {"は": "topic marker", "を": "object marker"},
    }
    
    # Apply fixes
    for orig, better in corrections.get(target_lang, {}).items():
        text = text.replace(orig, better)
    
    return text

# ✅ Solution 4: Use Hybrid Translation
# Combine multiple models and pick best output
models = ["Opus-MT", "mBART", "FLAN-T5"]
outputs = [translate_with_model(text, model) for model in models]
best = select_best_translation(outputs)
```

### Problem: Titles/Signs Not Translated

**Symptoms:**
- Text on screen stays in Japanese
- Character names not translated
- Signs/subtitles missing

**Cause:**
- OCR required (separate step)
- Not part of dialogue
- Not in transcription

**Solutions:**

```python
# ✅ Solution 1: Manual Subtitle Creation
# Create SRT file manually:
srt_content = """
1
00:00:01,000 --> 00:00:03,000
English subtitle

2
00:00:04,000 --> 00:00:06,000
Next subtitle
"""

with open("output.srt", "w") as f:
    f.write(srt_content)

# ✅ Solution 2: Use OCR for On-Screen Text
from pytesseract import pytesseract

def ocr_video(video_path):
    cap = cv2.VideoCapture(video_path)
    texts = []
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        
        text = pytesseract.image_to_string(frame)
        if text.strip():
            texts.append(text)
    
    return texts

# ✅ Solution 3: Keep Original Subtitles
# Don't overlay dubbed subs, keep original
# Just change audio
```

---

## 📱 Google Colab Specific Issues

### Problem: "Gradio Link Not Generated"

**Symptoms:**
- No public URL in output
- Only local URL shown
- Can't access from browser

**Cause:**
- Gradio not configured for sharing
- Network issue

**Solutions:**

```python
# ✅ Solution 1: Force Sharing
from gradio import Interface

# In code, change:
demo.launch(share=True)  # Add share=True

# ✅ Solution 2: Use Gradio Tunnel
# Install:
!pip install gradio-tunneling

# Use:
import gradio.tunneling
```

### Problem: "Colab Runtime Disconnected"

**Symptoms:**
- "Runtime disconnected"
- Lost all progress
- Need to start over

**Cause:**
- Idle timeout (90 minutes)
- Manual disconnection
- Network issue

**Solutions:**

```python
# ✅ Solution 1: Run in Background
# Keep Colab tab active during processing

# ✅ Solution 2: Use Colab Pro
# Higher timeout (up to 24 hours)

# ✅ Solution 3: Save Progress
import pickle

# Save state after each step
with open("/tmp/progress.pkl", "wb") as f:
    pickle.dump({
        "segments": segments,
        "cloned": cloned_segments,
        "timestamp": time.time()
    }, f)

# Load and resume
with open("/tmp/progress.pkl", "rb") as f:
    state = pickle.load(f)
```

---

## Performance Issues

### Problem: Processing Takes 3+ Hours

**Symptoms:**
- Still processing after 3 hours
- Percentage stuck
- No visible progress

**Cause:**
- Video too long
- Model too large
- Hardware struggling

**Solutions:**

```python
# ✅ Solution 1: Use Faster Settings
whisper_model = "tiny"      # Fastest
batch_size = 4              # Process multiple at once

# ✅ Solution 2: Split Video
# Process 2-minute chunks separately
# Then combine results

# ✅ Solution 3: Profile Processing
import time

times = {
    "download": 0,
    "audio_extract": 0,
    "transcribe": 0,
    "translate": 0,
    "voice_clone": 0,
    "mixing": 0,
    "video_create": 0
}

# Track each step
start = time.time()
# ... do step ...
times["step_name"] = time.time() - start

print(times)  # See where time is spent
```

---

## Emergency Troubleshooting

### If Nothing Works

```python
# 🆘 Emergency Reset
import subprocess
import shutil
import os

# Clear cache
shutil.rmtree("/tmp/.config", ignore_errors=True)
shutil.rmtree("/tmp/huggingface", ignore_errors=True)
shutil.rmtree("/tmp/transformers", ignore_errors=True)

# Restart Colab kernel
from google.colab import runtime
runtime.restart()

# Run again
```

---

## Getting Help

**If issue persists:**

1. ✅ Read error message VERY carefully
2. ✅ Search in this document (Ctrl+F)
3. ✅ Try smaller test video (30 seconds)
4. ✅ Check internet connection
5. ✅ Restart Colab kernel
6. ✅ Try Colab Pro
7. ✅ Use CPU instead of GPU

---

**Remember:** Start small, test, then scale up! 🎬✨
