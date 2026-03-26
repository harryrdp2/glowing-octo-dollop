# 🎬 DubSync Gradio - Google Colab Quick Start

## ⚡ सिर्फ 3 स्टेप में चलाओ!

### Step 1️⃣ Google Colab खोलो
https://colab.research.google.com

### Step 2️⃣ इस कोड को Copy-Paste करो:

```python
# Step 1: Install dependencies
print("📦 Installing packages...")
!pip install -q gradio torch torchaudio transformers librosa pydub moviepy
!pip install -q demucs f5-tts yt-dlp ffmpeg-python scipy numpy sentencepiece protobuf noisereduce
!apt-get update && apt-get install -y ffmpeg sox libsox-fmt-all 2>/dev/null

# Step 2: Clone DubSync
print("\n📥 Cloning DubSync...")
!cd /content && git clone https://github.com/harryrdp2/DubSync.git 2>/dev/null || echo "Already exists"

# Step 3: Download Whisper models (one-time)
print("\n🎤 Preloading Whisper model...")
import whisper
whisper.load_model("base")

print("\n" + "="*60)
print("✅ Setup Complete!")
print("="*60)
print("\n🚀 Run this in the NEXT cell:\n")
print("   %cd /content/DubSync/DubSync")
print("   !python app_gradio.py")
print("\n" + "="*60)
```

**यह cell 10-15 minutes लेगा। Wait करो!** ⏳

### Step 3️⃣ अगले Cell में यह code चलाओ:

```python
%cd /content/DubSync/DubSync
!python app_gradio.py
```

**Link click करो जो नीचे दिखेगा!** 🔗

---

## 🎯 कैसे Use करें?

1. **Video URL डालो** - YouTube या कोई भी video link
2. **Source Language चुनो** - Japanese, English, Chinese, etc.
3. **Target Language चुनो** - English, Chinese, Hindi
4. **Whisper Model चुनो**:
   - `tiny` - Super fast (~2 min)
   - `base` - Fast (~5 min) ⭐ Recommended
   - `small` - Better (~10 min)
   - `medium` - Best quality (~20 min)

5. **"🚀 Process Video" क्लिक करो** - Wait करो! 
6. **Dubbed video download करो** ✨

---

## ⏱️ Processing Time

- **First Run**: Model download (~10 min)
- **Processing**: 15-45 minutes (video length पर depend करता है)
- **Shorter videos**: तेजी से process होंगे
- **GPU enabled**: ~5-10x faster!

---

## 🌍 Supported Languages

### Input (Original Video):
- Japanese 🇯🇵
- English 🇬🇧
- Chinese 🇨🇳
- Korean 🇰🇷
- Spanish 🇪🇸
- French 🇫🇷
- Hindi 🇮🇳
- German 🇩🇪
- And many more!

### Output (Dubbed Video):
- English 🇬🇧
- Chinese 🇨🇳
- Hindi 🇮🇳

---

## 💡 Tips & Tricks

### Speed बढ़ाने के लिए:
1. Smaller Whisper model use करो (`base` की जगह `tiny`)
2. 2-3 minute का video try करो
3. GPU Runtime enable करो (Settings → Runtime type → GPU)

### Quality बढ़ाने के लिए:
1. Larger Whisper model use करो (`large` या `medium`)
2. Clear audio वाला video use करो
3. F5-TTS को time दो (queue में लग सकता है)

### Cost बचाने के लिए:
1. Free Colab tier में 12 hours तक काम कर सकते हो
2. Model एक बार download हो जाए तो fast हो जाता है
3. Colab+ subscribe करो longer sessions के लिए

---

## 🔧 Troubleshooting

### "CUDA out of memory"
```python
# Smaller model try करो
# या Colab kernel restart करो
```

### "ffmpeg: command not found"
```python
!apt-get install -y ffmpeg
```

### "Model download failed"
```python
# Internet connection check करो
# या later फिर se try करो
```

### "Processing is slow"
- Smaller Whisper model use करो
- Shorter video try करो
- GPU runtime enable करो

---

## 📊 Gradio vs Streamlit

| Feature | Streamlit | Gradio |
|---------|-----------|--------|
| **Colab URL** | ⚠️ Requires ngrok | ✅ Automatic |
| **Setup** | ⚠️ Complex | ✅ Simple |
| **Speed** | ⚠️ Slower | ✅ Faster |
| **Public Link** | ❌ No | ✅ Yes |
| **Best For** | Desktop apps | Colab |

**Gradio का यह version Colab के लिए बेहतर है!**

---

## 🎬 Example Usage

### Example 1: Japanese Anime → English
```
Video: YouTube anime clip
Source: Japanese
Target: English
Model: base
Result: English dubbed anime
```

### Example 2: Quick Test
```
Video: 1-minute clip
Source: English
Target: Chinese
Model: tiny
Result: Fast processing
```

### Example 3: Best Quality
```
Video: Full video
Source: English
Target: Hindi
Model: medium
Result: High quality dubbing
```

---

## 📥 Results Download करना

Processing के बाद ये files मिलेंगे:

1. **Dubbed Video** (`dubbed_en.mp4`)
   - Complete dubbed version
   - Original music + new voices
   - Ready to share!

2. **Subtitles** (`subtitles_en.srt`)
   - Video players में use करो
   - Translation display करेगा

3. **Transcription CSV**
   - Original text
   - Translated text
   - Timing information

---

## 💰 Cost

- ✅ **Free!** 🎉
- ✅ No API charges
- ✅ No setup fees
- ✅ Google Colab का free tier काफी है
- **Total Cost: $0**

---

## ❓ FAQ

**Q: क्या internet requirement है?**
A: हां, model download के लिए। बाकी सब local है।

**Q: Processing के बीच में internet बंद हो गया?**
A: Colab disconnect हो जाएगा। फिर से शुरू करना पड़ेगा।

**Q: कौन-कौन से languages supported हैं?**
A: 100+ language pairs (Helsinki-NLP से)। Plus में जोड़ सकते हो।

**Q: क्या original file safe है?**
A: हां! सिर्फ dubbing होता है, original नहीं बदलता।

**Q: Gradient vs Streamlit कौन better है?**
A: Colab के लिए Gradio better है। Auto URL, faster, simpler!

---

## 🚀 Advanced Tips

### Custom Language Pair Add करना:
Edit `app_gradio.py` में language dropdown:
```python
"French": "fr",
"German": "de",
# Add your language here
```

### Batch Processing:
एक एक video के साथ पूरा process करो।

### Results Save करना:
Download button से save करो या Google Drive में upload करो।

---

## 📚 अधिक जानकारी

- Full guide: `README_COLAB.md`
- Technical details: `CHANGES.md`
- File guide: `FILE_GUIDE.md`

---

## ⚡ One-Liner Setup

Copy-paste करो एक ही cell में:

```python
!pip install -q gradio torch transformers librosa pydub moviepy demucs f5-tts yt-dlp ffmpeg-python scipy numpy sentencepiece && !apt-get install -y ffmpeg 2>/dev/null && !git clone https://github.com/harryrdp2/DubSync.git /content/DubSync 2>/dev/null && cd /content/DubSync/DubSync && python app_gradio.py
```

---

**Ready? 🎬 Start DubSync और अपने videos को dub करो!**

*"AI से video dubbing, बिना API, बिना cost!"*
