# 🎬 DubSync Advanced Anime Dubbing Guide

## विषये (Overview)

आपका **Advanced Anime Dubbing Engine** है जो **professional-quality dubbing** देता है:

```
🎭 Per-Character Voice Cloning
├─ हर character का अलग voice clone
├─ Original voice से emotion capture
└─ Real human dubbing जैसा quality

🎵 Audio Layer Separation
├─ Vocals अलग
├─ Background music intact
└─ Sound effects preserved

😊 Emotion Preservation
├─ Anger, Happy, Sad, Excited detection
├─ Voice modulation per emotion
└─ Authentic character expression

📊 Advanced Lip-Sync
├─ Frame-by-frame matching
├─ Mouth movement sync
└─ Speech timing perfect

🌐 Multi-Language Support
├─ Japanese → Hindi/English
├─ Character names auto-detected
└─ Emotion aware translation
```

---

## 📋 Features Explained

### 1. **Character Voice Cloning** 🎭

**कैसे काम करता है:**

```
Original Audio (Japanese)
    ↓
Character Detection
    ↓
Extract Current Voice
    ↓
Convert Text to Hindi
    ↓
Clone Voice with Emotion
    ↓
Output Hindi Voice (Authentic)
```

**उदाहरण:**
- Taro का original voice: deep, serious, young male
- Dubbed में: Same character के लिए same voice personality
- F5-TTS से: Zero training with reference audio

### 2. **Audio Separation** 🎵

Demucs AI से 4 layers अलग होते हैं:

```
Original Audio
    ↓
├─ Vocals (dialogue)
├─ Drums (percussion)
├─ Bass (low frequencies)
└─ Other (background, effects)

Process:
Vocals → Dubbing के लिए translate करो
Other → Original रखो mixing में
```

### 3. **Emotion Detection & Preservation** 😊

**Detected Emotions:**

| Text में | Audio में | Output में |
|---------|----------|-----------|
| "!" (क्रोध) | Pitch +30% | तेज़, aggressive |
| "^_^" (खुश) | Pitch +20% | Light, energetic |
| "..." (उदास) | Pitch -20% | Slow, melancholic |
| "?" (confused) | Pitch variation | Questioning tone |

**Formula:**
```
Emotion = Detect(text keywords) + Detect(audio patterns)
Output Voice = Clone(original voice) + Modify(emotion params)
```

### 4. **Lip-Sync Matching** 📊

**Detection Points:**
- Onset detection: mouth opening
- Voiced frames: speaking moments
- Timing: frame-perfect sync
- Intensity: mouth movement intensity

**Result:** HD anime लगता है lab-synced perfectly

---

## 🚀 Quick Start (Google Colab)

### Step 1️⃣: Setup और Run

```python
# Cell 1: Install dependencies
!pip install git+https://github.com/f5-tts/F5-TTS.git
!pip install demucs librosa pydub yt-dlp gradio transformers torch

# Cell 2: Clone and run DubSync
!cd /tmp && git clone <your-repo> DubSync
%cd /tmp/DubSync
!python app_advanced_anime_dub.py
```

### Step 2️⃣: Access Gradio

```
Output:
Running on public URL: https://xxxxx-gradio-link.gradio.live
```

Copy URL → Browser में खोलो

### Step 3️⃣: Configure

```json
Video URL: https://youtube.com/watch?v=xxxxx

Character JSON:
{
  "taro": {"name": "Taro", "voice_type": "young_male"},
  "yuki": {"name": "Yuki", "voice_type": "young_female"},
  "villain": {"name": "Villain", "voice_type": "old_male"}
}

Source: Japanese
Target: Hindi
```

### Step 4️⃣: Process

- Upload करो या YouTube URL दो
- "Start Dubbing" click करो
- **30-90 minutes** (video length पर depend करता है)
- Download करो dubbed video + transcription CSV

---

## 🎯 Advanced Configuration

### Character Profile JSON

```json
{
  "character_1": {
    "name": "Protagonist",
    "voice_type": "young_male",
    "pitch_adjust": 1.0,
    "speed": 0.9,
    "energy": 1.1
  },
  "character_2": {
    "name": "Heroine",
    "voice_type": "young_female",
    "pitch_adjust": 1.1,
    "speed": 0.95,
    "energy": 1.0
  }
}
```

**Fields:**
- `name`: Character का नाम (auto-detection के लिए)
- `voice_type`: male/female/child (future use)
- `pitch_adjust`: Voice pitch (1.0 = original)
- `speed`: Speech speed (0.8-1.2)
- `energy`: Volume/energy (0.5-1.5)

### Emotion Parameters

```python
Emotions = {
    "angry": {
        "pitch": 1.3,      # High pitch
        "speed": 1.1,      # Faster
        "energy": 1.4      # Loud
    },
    "happy": {
        "pitch": 1.2,      # Slightly high
        "speed": 0.95,     # Normal
        "energy": 1.2      # Bright
    },
    "sad": {
        "pitch": 0.8,      # Lower
        "speed": 0.9,      # Slower
        "energy": 0.7      # Soft
    },
    "whisper": {
        "pitch": 0.9,      # Normal
        "speed": 1.0,      # Normal
        "energy": 0.5      # Very soft
    },
    "excited": {
        "pitch": 1.4,      # High
        "speed": 1.2,      # Fast
        "energy": 1.5      # Very loud
    }
}
```

---

## 📊 Output Files

### 1. **Dubbed Video** 🎬
```
dubbed_[lang_code].mp4

Example: dubbed_hi.mp4 (Hindi)

Includes:
✅ Character voices (dubbed)
✅ Background music
✅ Sound effects
✅ Lip-sync aligned
✅ Emotion preserved
```

### 2. **Transcription CSV** 📝

```
ID | Character | Emotion  | Original    | Translation    | Start | End
1  | taro      | neutral  | "Ohayo!"    | "नमस्ते!"     | 0.0s  | 1.2s
2  | yuki      | happy    | "Good"      | "अच्छा है!"    | 1.5s  | 2.8s
3  | taro      | angry    | "No!!"      | "नहीं!!"       | 3.0s  | 3.5s
```

---

## 🎨 How It Works (Technical)

### Phase 1: Audio Processing

```
Raw Audio
    ↓
Demucs Separation
    ├─ Vocals (dialogue)
    ├─ Drums
    ├─ Bass
    └─ Other (music, effects)
    ↓
Status: "🎵 Separating audio layers..."
```

### Phase 2: Transcription & Character Detection

```
Vocals Stream
    ↓
Whisper Model (whisper-base/medium/large)
    ↓
Transcription with Timestamps
    ├─ Text: "これは素晴らしい"
    ├─ Speaker: character_1 (auto-detect)
    ├─ Emotion: "happy"
    └─ Time: 5.2s - 6.8s
    ↓
Status: "🎤 Transcribing audio..."
```

### Phase 3: Translation

```
Transcription Segments
    ↓
Helsinki-NLP Opus-MT Model
    ├─ Model: Helsinki-NLP/Opus-MT-ja-hi
    ├─ Input: "これは素晴らしい" (Japanese)
    └─ Output: "यह शानदार है" (Hindi)
    ↓
Preserve Emotion Tags
    ↓
Status: "🌐 Translating with emotion..."
```

### Phase 4: Voice Cloning Per Character

```
For Each Segment:
    1. Extract character's original audio clip
    2. Get voice characteristics (pitch, energy, tempo)
    3. Get emotion (from text/audio)
    4. Run F5-TTS with:
       - Reference audio: original character voice
       - Reference text: original dialogue
       - Generate text: translated dialogue
       - Speed: 0.8 (clear enunciation)
    5. Adjust output for emotion:
       - pitch_shift()
       - time_stretch()
       - energy modulation
    6. Save cloned audio
    ↓
Status: "🎭 Voice cloning: 45/50"
```

### Phase 5: Audio Mixing

```
Cloned Dialogues (per character)
    ↓
Mix Timeline:
├─ 0.0-1.2s: Taro's dubbed voice
├─ 1.2-2.8s: Yuki's dubbed voice
├─ 2.8-3.5s: Taro's dubbed voice (angry)
└─ ...continues
    ↓
Combine with:
├─ Background Music (original)
├─ Sound Effects (original)
└─ Ambient Audio
    ↓
Mixed Audio Stream
```

### Phase 6: Video Composition

```
Original Video
    + 
New Audio (dubbed)
    ↓
Encode:
├─ Codec: libx264 (high quality)
├─ Audio: AAC (stereo)
└─ Bitrate: Auto
    ↓
Output: dubbed_[lang].mp4
```

---

## 🎯 Language Support

### Supported Pairs:

| From | To | Status |
|------|----|----|
| Japanese | Hindi | ✅ Full |
| Japanese | English | ✅ Full |
| Japanese | Chinese | ✅ Full |
| English | Hindi | ✅ Full |
| Korean | Hindi | ✅ Full |
| Chinese | Hindi | ✅ Full |

### Add New Language:

1. Check Helsinki-NLP models
2. Update `lang_map` in code
3. Use `Helsinki-NLP/Opus-MT-[from]-[to]`

```python
lang_map = {
    "Japanese": "ja",
    "English": "en",
    "Chinese": "zh",
    "Hindi": "hi",
    "Korean": "ko",
    "Spanish": "es",  # Add new
    "French": "fr",   # Add new
}
```

---

## ⚙️ System Requirements

### For Google Colab (GPU):

```
📊 Minimum:
├─ RAM: 8 GB
├─ GPU Memory: 6 GB (free tier T4)
├─ Disk: 20 GB temp space
└─ Runtime: 2-3 hours

📈 Recommended:
├─ RAM: 16 GB
├─ GPU Memory: 12+ GB (A100)
├─ Disk: 50 GB
└─ Runtime: 30-90 min
```

### Models & Sizes:

```
Whisper-base:      ~140 MB
Whisper-medium:    ~390 MB
Helsinki-NLP:      ~60-80 MB (per model)
F5-TTS:            ~500 MB
Demucs:            ~300 MB

Total: ~1.5-2 GB (downloads को cache होता है)
```

---

## 🐛 Troubleshooting

### समस्या 1: Out of Memory

**Error:** `CUDA out of memory`

**समाधान:**
```
1. Reduce whisper_model size:
   "base" → "tiny"

2. Process shorter video:
   < 5 minutes

3. Use CPU (slower):
   !export CUDA_VISIBLE_DEVICES=""
```

### समस्या 2: Bad Audio Quality

**समस्या:** Dubbed audio सुनने में अजीब लगे

**समाधान:**
```python
# Adjust parameters in voice cloning:
- speed उदाहरण: 0.8 (स्पष्टता के लिए)
- pitch_shift समायोजन अपनी जरूरत से करें
- Emotion preservation check करें
```

### समस्या 3: Character Not Detected

**Error:** "Character character_2 not found"

**समाधान:**
```json
{
  "char1": {"name": "Taro"},      // Correct format
  "char2": {"name": "Yuki"}       // Correct ID
}

Check:
- Character JSON syntax
- Character names in video
- Speaker detection settings
```

### समस्या 4: Lip-Sync Not Perfect

**समस्या:** Lips सिंक में नहीं हैं

**समाधान:**
```
1. Slow down speech:
   speed = 0.8-0.85

2. Adjust timing:
   Segment duration match करें

3. Use smaller whisper_model:
   More precise timestamps
```

---

## 🎬 Use Cases

### 1. **Japanese Anime → Hindi Dubbing** 🇯🇵→🇮🇳

```
Original: Naruto (Japanese)
Output: Naruto (Hindi) - एनिमे के साथ
Characters: Naruto, Sasuke, Sakura आदि
Quality: TV-broadcast ready
```

### 2. **English Content → Multiple Languages**

```
Original: English anime
Output 1: Hindi version
Output 2: Spanish version
Output 3: French version
```

### 3. **Character Customization** 🎭

```
Same anime, different voice settings:
- Softer tone for one character
- Aggressive tone for another
- Child voice for younger character
- Character-specific pitch adjustment
```

---

## 📈 Performance Tips

### 1. **Shorter Videos** (Better for first time)
```
1-2 minutes: ~15-30 minutes processing
5 minutes: ~30-60 minutes
10+ minutes: 1.5-3 hours
```

### 2. **Parallel Processing** (Future)
```
# Coming soon: Process multiple characters simultaneously
# Currently: Sequential per-character processing
```

### 3. **Model Caching**
```
First run: Download models (~2GB)
Next runs: Use cached models (instant)
```

---

## 📚 Code Examples

### Adding Custom Characters

```python
dubber = AdvancedAnimeDubber()

# Method 1: JSON
dubber.add_character("char1", "Protagonist")

# Method 2: With voice sample (future)
dubber.add_character("char2", "Heroine", voice_path="/path/to/sample.wav")
```

### Custom Emotion Mapping

```python
# Override default emotions
emotion_mapping = {
    "shouting": "angry",
    "laughing": "happy",
    "sobbing": "sad",
    "whispered": "whisper"
}
```

### Advanced Voice Adjustment

```python
params = {
    "pitch": 1.2,      # Hero voice
    "speed": 0.9,      # Natural speed
    "energy": 1.1      # Bold
}
```

---

## 🌟 Quality Checklist

Before publishing dubbed video:

- [ ] ✅ सभी characters सही voice में हैं
- [ ] ✅ Emotions authentic लगते हैं
- [ ] ✅ Lips हर word के साथ match करते हैं
- [ ] ✅ Background music intact है
- [ ] ✅ Sound effects clear हैं
- [ ] ✅ No glitches या disconnections
- [ ] ✅ Audio volume normalized है
- [ ] ✅ Timing proper है (no gaps/overlaps)

---

## 🚀 Next Steps

1. **Try Basic Version First:**
   - Short 2-minute anime clip
   - Test with 2 characters
   - Verify quality

2. **Then Scale Up:**
   - Longer videos
   - More characters
   - Experiment with emotions

3. **Optimize:**
   - Fine-tune pitch per character
   - Adjust speed settings
   - Perfect lip-sync

4. **Share Results:**
   - Get feedback
   - Improve params
   - Perfect the dubbing

---

## 📞 Support

**Issues या Error?**
1. Check troubleshooting section
2. Read error message carefully
3. Verify input format
4. Check system requirements
5. Try with smaller video first

---

## 📖 Additional Resources

- **F5-TTS Docs:** Voice cloning parameters
- **Whisper Docs:** Transcription options
- **Demucs Docs:** Audio separation
- **Helsinki-NLP:** Translation models

---

**Made with ❤️ for anime dubbers everywhere!**

**Version:** Advanced 2.0
**Last Updated:** 2026
**Status:** Production Ready ✅
