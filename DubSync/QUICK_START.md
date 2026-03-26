# Quick Start Guide - DubSync on Google Colab

## ⚡ 5-Minute Setup (Copy-Paste)

### Step 1: Create a New Google Colab Notebook
Go to https://colab.research.google.com and create a new notebook.

### Step 2: Run This Cell
Copy and paste this entire code block into the first cell:

```python
# Step 1: Install dependencies
print("📦 Installing dependencies...")
!pip install -q torch torchaudio
!pip install -q transformers librosa pydub moviepy demucs f5-tts
!pip install -q streamlit sentencepiece protobuf yt-dlp ffmpeg-python scipy numpy noisereduce requests
!apt-get update && apt-get install -y ffmpeg sox libsox-fmt-all 2>/dev/null

# Step 2: Clone DubSync
print("\n📥 Cloning DubSync...")
!cd /content && git clone https://github.com/harryrdp2/DubSync.git 2>/dev/null || echo "Already exists"

# Step 3: Verify installation
print("\n✅ Installation complete!")
import torch
print(f"GPU Available: {torch.cuda.is_available()}")

print("\n" + "="*60)
print("🎬 Ready to run DubSync!")
print("="*60)
print("\nRun this in the NEXT cell:\n")
print("    %cd /content/DubSync/DubSync")
print("    !streamlit run app_colab.py --logger.level=error")
print("\n" + "="*60)
```

**This cell will take 10-15 minutes to run.** Wait for it to complete.

### Step 3: Run DubSync in Next Cell
```python
%cd /content/DubSync/DubSync
!streamlit run app_colab.py --logger.level=error
```

Click the **Streamlit URL** that appears to open the interface!

---

## 🎯 Usage

1. **Paste Video URL** - YouTube or any video link
2. **Select Languages** - Source (Japanese/English/etc) → Target (English/Chinese/etc)
3. **Choose Whisper Model** - Pick based on speed vs quality:
   - `tiny`: Super fast (~2 mins)
   - `base`: Fast (~5 mins)
   - `small`: Good (~10 mins)
   - `medium`: Best (~20 mins)

4. **Enable/Disable Audio Cleaning** - Check for better transcription
5. **Click Process Button** - Wait for magic! ✨

Result will show in the app when done!

---

## 💡 Important Notes

### ⏱️ Processing Time
- First run: Download models (2-3 GB, ~10 min)
- Subsequent runs: Skip downloads (faster)
- Processing: 15-45 mins depending on video length & model

### 🎬 Video Guidelines
- **Format**: MP4, MKV, AVI, WebM (via YouTube)
- **Length**: Works best with 2-5 minute clips
- **Quality**: Source quality affects output

### 🎯 Language Support
**Input languages**: Japanese, English, Chinese, Korean, Spanish, French, German, Italian, Portuguese, Russian, Arabic, Hindi

**Output languages**: 
- English (en)
- Chinese (zh)
- Hindi (hi)

### ⚙️ GPU Tips
- **Use GPU Runtime** - Settings → Runtime type → GPU
- **A100 with Colab+** - Much faster processing
- **Free tier GPU** - Good for learning, slower for long videos

---

## 🔧 Troubleshooting

### "Streamlit is not found"
Run the installation cell again and wait for it to complete.

### "CUDA out of memory"
```python
# Use smaller Whisper model (base instead of medium)
# Or restart Colab kernel: Runtime → Restart session
```

### "Video download failed"
- Use YouTube links (more reliable)
- Check internet connection
- Try different video

### "ffmpeg not found"
```python
!apt-get install -y ffmpeg
```

### Processing takes forever
- Use smaller Whisper model
- Use shorter video clip
- Use A100 GPU (Colab+)

---

## 📥 Download Results

After processing completes:

1. **Dubbed Video** - Download directly from interface
2. **Transcription CSV** - Has original + translation + timing
3. **Subtitle File** - SRT format for video players

Click the "📥 Download" buttons in the app!

---

## 💰 Cost
**Completely Free!** 🎉
- No API keys needed
- No monthly charges
- No credit card required
- All models open-source

---

## 📚 Full Documentation
For detailed setup and advanced options, see:
- `README_COLAB.md` - Complete Colab guide
- `CHANGES.md` - What's different from original
- `README.md` - Original DubSync documentation

---

## ⚡ Advanced: Custom Setup Script
Alternatively, use the automated setup script:

```python
!git clone https://github.com/harryrdp2/DubSync.git /content/dubsync
%cd /content/dubsync/DubSync
!python colab_setup.py
```

Then run Streamlit as shown above.

---

## 🚀 Next Steps
1. Test with a short YouTube video
2. Try different Whisper models for quality
3. Experiment with different languages
4. Customize settings as needed

---

## ❓ FAQ

**Q: Do I need an API key?**  
A: Nope! Everything is local.

**Q: How long does it take?**  
A: First run ~30 mins (downloading models). Typical video: 15-45 mins.

**Q: Can I save videos to Drive?**  
A: Yes! Download from Streamlit interface, then upload to Drive.

**Q: What if connection drops?**  
A: You may need to restart and re-run. Use Colab+ for more stable sessions.

**Q: Can I use CPU only?**  
A: Yes, but it's 5-10x slower. GPU strongly recommended.

---

**Ready to dub? Follow the 3 steps above and enjoy! 🎬✨**
