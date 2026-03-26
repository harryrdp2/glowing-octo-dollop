"""
DubSync - Google Colab Version with Gradio UI (No API Required)
Better for Colab - creates automatic public URL
"""

import os
import sys
import gradio as gr

# Set environment variables for writable paths (Colab compatible)
os.environ["XDG_CONFIG_HOME"] = "/tmp/.config"
os.environ["XDG_CACHE_HOME"] = "/tmp/.cache"
os.environ["HF_HOME"] = "/tmp/huggingface"
os.environ["HF_HUB_CACHE"] = "/tmp/huggingface/hub"
os.environ["TRANSFORMERS_CACHE"] = "/tmp/transformers"
os.environ["TORCH_HOME"] = "/tmp/torch"
os.environ["MPLCONFIGDIR"] = "/tmp/matplotlib"

# Make sure directories exist
for path in [
    os.environ["XDG_CONFIG_HOME"],
    os.environ["XDG_CACHE_HOME"],
    os.environ["HF_HOME"],
    os.environ["HF_HUB_CACHE"],
    os.environ["TRANSFORMERS_CACHE"],
    os.environ["TORCH_HOME"],
    os.environ["MPLCONFIGDIR"],
]:
    os.makedirs(path, exist_ok=True)

import subprocess
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip
import whisper
from pydub import AudioSegment
import shutil
import yt_dlp
import time
import torch
import pandas as pd
import json
import numpy as np
import librosa
from scipy.signal import butter, filtfilt
from transformers import MarianMTModel, MarianTokenizer
import warnings
warnings.filterwarnings('ignore')

print("🎬 DubSync Gradio - Starting up...\n")

device = "cuda" if torch.cuda.is_available() else "cpu"
print(f"✅ Device: {device.upper()}")
if device == "cuda":
    print(f"✅ GPU: {torch.cuda.get_device_name(0)}")

os.makedirs(os.environ["XDG_CACHE_HOME"], exist_ok=True)
temp_folder = os.path.join("/tmp", "dubsync_resources")
sample_output_dir = os.path.join(temp_folder, "outputs")
cropped_audio_dir = os.path.join(temp_folder, "cropped_audio")
cloned_audio_dir = os.path.join(temp_folder, "cloned_audio")

os.makedirs(temp_folder, exist_ok=True)
os.makedirs(cropped_audio_dir, exist_ok=True)
os.makedirs(cloned_audio_dir, exist_ok=True)
os.makedirs(sample_output_dir, exist_ok=True)

# Global model cache
_translation_model_cache = {}
_processing = False

def get_translation_model(model_name):
    """Load and cache translation model"""
    if model_name not in _translation_model_cache:
        try:
            print(f"📥 Loading translation model: {model_name}")
            tokenizer = MarianTokenizer.from_pretrained(model_name)
            model = MarianMTModel.from_pretrained(model_name).to(device)
            _translation_model_cache[model_name] = (model, tokenizer)
            print(f"✅ Model loaded successfully!")
        except Exception as e:
            print(f"❌ Error loading model {model_name}: {e}")
            return None, None
    
    return _translation_model_cache[model_name]

def translate_text_local(texts, source_lang_code, target_lang_code):
    """Translate text using local models"""
    model_name = f"Helsinki-NLP/Opus-MT-{source_lang_code}-{target_lang_code}"
    
    try:
        model, tokenizer = get_translation_model(model_name)
        if model is None:
            print(f"⚠️ Translation model not available")
            return texts
        
        inputs = tokenizer(texts, return_tensors="pt", padding=True).to(device)
        with torch.no_grad():
            outputs = model.generate(**inputs)
        
        translated = tokenizer.batch_decode(outputs, skip_special_tokens=True)
        return translated
    except Exception as e:
        print(f"❌ Translation error: {e}")
        return texts

def download_video(video_url):
    """Download video from YouTube or URL"""
    print(f"📥 Downloading video from: {video_url}")
    uploaded_video_path = os.path.join(temp_folder, "uploaded_video.mp4")
    
    try:
        if "youtube.com" in video_url or "youtu.be" in video_url:
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': os.path.join(temp_folder, "uploaded_video"),
                'merge_output_format': 'mp4',
                'quiet': True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                video_file = ydl.prepare_filename(info)
            print(f"✅ Downloaded: {info.get('title', 'Video')}")
            return video_file
        else:
            import requests
            response = requests.get(video_url, stream=True, timeout=30)
            if response.status_code == 200:
                with open(uploaded_video_path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                print(f"✅ Video downloaded!")
                return uploaded_video_path
            else:
                return None
    except Exception as e:
        print(f"❌ Download error: {e}")
        return None

def extract_audio_from_video(video_path):
    """Extract audio from video"""
    print(f"🎬 Extracting audio...")
    try:
        video = VideoFileClip(video_path)
        audio_path = os.path.join(temp_folder, "extracted_audio.wav")
        video.audio.write_audiofile(audio_path, verbose=False, logger=None)
        print(f"✅ Audio extracted!")
        return audio_path
    except Exception as e:
        print(f"❌ Error extracting audio: {e}")
        return None

def separate_audio_layers(audio_path):
    """Separate audio using Demucs"""
    print(f"🎶 Separating audio layers...")
    output_dir = os.path.join(temp_folder, "demucs_output")
    try:
        subprocess.run(["demucs", "-o", output_dir, f"--device={device}", audio_path], 
                      capture_output=True, text=True)
        print(f"✅ Audio separated!")
        return output_dir
    except Exception as e:
        print(f"❌ Error separating audio: {e}")
        return None

def transcribe_audio(audio_path, model_name, language_code):
    """Transcribe audio using Whisper"""
    print(f"🎤 Transcribing audio with {model_name} model...")
    try:
        model = whisper.load_model(model_name, device=device)
        result = model.transcribe(audio_path, language=language_code, fp16=False)
        print(f"✅ Transcription complete! Found {len(result['segments'])} segments")
        return result["segments"]
    except Exception as e:
        print(f"❌ Transcription error: {e}")
        return []

def translate_segments(segments, source_code, target_code):
    """Translate all segments"""
    print(f"🌐 Translating segments...")
    texts = [seg["text"] for seg in segments]
    translated_texts = translate_text_local(texts, source_code, target_code)
    
    for i, seg in enumerate(segments):
        seg["translation"] = translated_texts[i] if i < len(translated_texts) else seg["text"]
    
    print(f"✅ Translation complete!")
    return segments

def run_f5_tts(ref_audio, ref_text, gen_text, output_file):
    """Run F5-TTS voice cloning"""
    try:
        command = [
            "f5-tts_infer-cli",
            "--model", "F5TTS_v1_Base",
            "--ref_audio", ref_audio,
            "--ref_text", ref_text,
            "--gen_text", gen_text,
            "--speed", "0.8",
            "--output_file", output_file
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ F5-TTS error: {e.stderr}")
        return False

def voice_cloning(segments, audio_path):
    """Clone voices for all segments"""
    print(f"🔊 Starting voice cloning...")
    audio = AudioSegment.from_file(audio_path)
    
    print(f"🔊 Cropping audio segments...")
    for segment in segments:
        try:
            start_ms = int(segment["start"] * 1000)
            end_ms = int(segment["end"] * 1000)
            cropped = audio[start_ms:end_ms]
            cropped.export(
                os.path.join(cropped_audio_dir, f"cropped_{segment['id']}.wav"),
                format="wav"
            )
        except Exception as e:
            print(f"⚠️ Could not crop segment {segment['id']}: {e}")
    
    print(f"🤖 Cloning voices...")
    success_count = 0
    for i, segment in enumerate(segments):
        try:
            ref_audio = os.path.join(cropped_audio_dir, f"cropped_{segment['id']}.wav")
            ref_text = segment["text"]
            gen_text = segment.get("translation", segment["text"])
            
            if not ref_text or not gen_text or not os.path.exists(ref_audio):
                continue
            
            output_file = os.path.join(cloned_audio_dir, f"output_{segment['id']}.wav")
            if run_f5_tts(ref_audio, ref_text, gen_text, output_file):
                success_count += 1
                print(f"✅ Segment {i+1}/{len(segments)} cloned")
        except Exception as e:
            print(f"⚠️ Error cloning segment {i}: {e}")
    
    print(f"✅ Voice cloning complete! ({success_count}/{len(segments)} segments)")
    return segments

def generate_audio_from_segments(segments, original_audio_path):
    """Generate final dubbed audio"""
    print(f"🌍 Generating dubbed audio...")
    try:
        translated_audio = os.path.join(temp_folder, "translated_audio.wav")
        final_audio = AudioSegment.silent(duration=0)
        last_end_time = 0
        
        for idx, segment in enumerate(segments):
            start_ms = segment["start"] * 1000
            end_ms = segment["end"] * 1000
            duration_ms = end_ms - start_ms
            
            audio_segment_path = os.path.join(cloned_audio_dir, f"output_{idx}.wav")
            if os.path.exists(audio_segment_path):
                spoken = AudioSegment.from_file(audio_segment_path)
            else:
                spoken = AudioSegment.silent(duration=int(duration_ms))
            
            gap_duration = start_ms - int(last_end_time * 1000)
            if gap_duration > 0:
                original_audio = AudioSegment.from_file(original_audio_path)
                gap_start = int(last_end_time * 1000)
                gap_end = int(start_ms)
                gap_audio = original_audio[gap_start:gap_end]
                final_audio += gap_audio
            
            if len(spoken) > duration_ms:
                spoken = spoken[:int(duration_ms)]
            else:
                spoken += AudioSegment.silent(duration=int(duration_ms - len(spoken)))
            
            final_audio += spoken
            last_end_time = segment["end"]
        
        final_audio.export(translated_audio, format="wav")
        print(f"✅ Audio generated!")
        return translated_audio
    except Exception as e:
        print(f"❌ Error generating audio: {e}")
        return None

def seconds_to_srt_time(seconds):
    """Convert seconds to SRT format"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"

def generate_srt_subtitles(segments, output_path, subtitle_type="translation"):
    """Generate SRT subtitle file"""
    try:
        with open(output_path, 'w', encoding='utf-8') as srt_file:
            for i, segment in enumerate(segments, 1):
                start_srt = seconds_to_srt_time(segment["start"])
                end_srt = seconds_to_srt_time(segment["end"])
                
                if subtitle_type == "translation" and "translation" in segment:
                    text = segment["translation"]
                else:
                    text = segment.get("text", "...")
                
                text = text.replace('\n', ' ').strip()
                if not text:
                    continue
                
                srt_file.write(f"{i}\n")
                srt_file.write(f"{start_srt} --> {end_srt}\n")
                srt_file.write(f"{text}\n\n")
        
        return output_path
    except Exception as e:
        print(f"❌ Error generating subtitles: {e}")
        return None

def process_video(video_url, source_lang, target_lang, whisper_model):
    """Main processing function"""
    global _processing
    
    if _processing:
        return "⚠️ Processing already in progress. Please wait.", None, None
    
    _processing = True
    start_time = time.time()
    
    try:
        print("\n" + "="*60)
        print(f"🎬 DubSync Processing Started")
        print(f"    Source: {source_lang} → Target: {target_lang}")
        print(f"    Model: {whisper_model}")
        print("="*60 + "\n")
        
        # Language code mapping
        lang_map = {
            "Japanese": "ja", "English": "en", "Chinese": "zh",
            "Korean": "ko", "Spanish": "es", "French": "fr",
            "Hindi": "hi", "German": "de", "Italian": "it",
            "Portuguese": "pt", "Russian": "ru", "Arabic": "ar"
        }
        
        source_code = lang_map.get(source_lang, "en")
        target_code = lang_map.get(target_lang, "en")
        
        # Step 1: Download video
        video_file = download_video(video_url)
        if not video_file:
            return "❌ Failed to download video", None, None
        
        # Step 2: Extract audio
        audio_path = extract_audio_from_video(video_file)
        if not audio_path:
            return "❌ Failed to extract audio", None, None
        
        # Step 3: Separate audio layers
        output_dir = separate_audio_layers(audio_path)
        if not output_dir:
            return "❌ Failed to separate audio", None, None
        
        # Get separated audio paths
        separated_dir = os.path.join(
            output_dir, "htdemucs", os.path.splitext(os.path.basename(audio_path))[0])
        vocals_path = os.path.join(separated_dir, "vocals.wav")
        bg_music_path = os.path.join(separated_dir, "other.wav")
        bass_path = os.path.join(separated_dir, "bass.wav")
        drums_path = os.path.join(separated_dir, "drums.wav")
        
        # Step 4: Transcribe
        segments = transcribe_audio(vocals_path, whisper_model, source_code)
        if not segments:
            return "❌ Transcription failed", None, None
        
        # Step 5: Translate
        segments = translate_segments(segments, source_code, target_code)
        
        # Step 6: Voice cloning
        segments = voice_cloning(segments, vocals_path)
        
        # Step 7: Generate dubbed audio
        translated_audio = generate_audio_from_segments(segments, audio_path)
        if not translated_audio:
            return "❌ Audio generation failed", None, None
        
        # Step 8: Create dubbed video
        print(f"🎬 Creating dubbed video...")
        video = VideoFileClip(video_file)
        translated_audio_clip = AudioFileClip(translated_audio)
        bg_audio = AudioFileClip(bg_music_path)
        drums_audio = AudioFileClip(drums_path)
        bass_audio = AudioFileClip(bass_path)
        
        combined_audio = CompositeAudioClip(
            [translated_audio_clip, bg_audio, drums_audio, bass_audio])
        video = video.with_audio(combined_audio)
        
        dubbed_video_path = os.path.join(
            sample_output_dir, f"dubbed_{target_code}.mp4")
        subtitle_path = os.path.join(
            sample_output_dir, f"subtitles_{target_code}.srt")
        
        generate_srt_subtitles(segments, subtitle_path)
        
        video.write_videofile(
            dubbed_video_path,
            codec="libx264",
            audio_codec="aac",
            verbose=False,
            logger=None
        )
        print(f"✅ Video created!")
        
        # Create results DataFrame
        results_data = [{
            "ID": s.get("id"),
            "Start": f"{s.get('start'):.2f}s",
            "End": f"{s.get('end'):.2f}s",
            "Original": s.get("text"),
            "Translation": s.get("translation"),
        } for s in segments]
        
        df = pd.DataFrame(results_data)
        
        # Calculate elapsed time
        elapsed_time = time.time() - start_time
        elapsed_minutes = round(elapsed_time / 60, 2)
        
        success_msg = f"""
✅ Processing Complete in {elapsed_minutes} minutes!

📊 Results:
• Segments processed: {len(segments)}
• Output video: dubbed_{target_code}.mp4
• Subtitles: subtitles_{target_code}.srt

🎬 Video ready for download!
"""
        
        _processing = False
        return success_msg, dubbed_video_path, df
        
    except Exception as e:
        print(f"❌ Error: {e}")
        _processing = False
        return f"❌ Processing error: {str(e)}", None, None

# Create Gradio Interface
def create_interface():
    """Create Gradio interface"""
    
    with gr.Blocks(title="🎬 DubSync - Gradio Edition", theme=gr.themes.Soft()) as demo:
        gr.HTML("""
        <div style="text-align: center; padding: 20px;">
            <h1>🎬 DubSync - AI Video Dubbing</h1>
            <p style="font-size: 16px; color: #666;">
                Transform your videos with AI-powered dubbing using local models (no API needed!)
            </p>
            <p style="color: #888; font-size: 14px;">
                📍 Running on: <b>{}</b> {} {}
            </p>
        </div>
        """.format(
            device.upper(),
            "| GPU:" if device == "cuda" else "",
            torch.cuda.get_device_name(0) if device == "cuda" else ""
        ))
        
        with gr.Row():
            with gr.Column(scale=1):
                gr.HTML("<h2>⚙️ Input Settings</h2>")
                
                video_url = gr.Textbox(
                    label="🎬 Video URL",
                    placeholder="Enter YouTube URL or video link...",
                    lines=1
                )
                
                source_lang = gr.Dropdown(
                    label="📍 Source Language",
                    choices=["Japanese", "English", "Chinese", "Korean", "Spanish", 
                            "French", "Hindi", "German", "Italian", "Portuguese", "Russian", "Arabic"],
                    value="Japanese"
                )
                
                target_lang = gr.Dropdown(
                    label="🌍 Target Language",
                    choices=["English", "Chinese", "Hindi"],
                    value="English"
                )
                
                whisper_model = gr.Dropdown(
                    label="🎤 Whisper Model",
                    choices=["tiny", "base", "small", "medium", "large"],
                    value="base",
                    info="Larger = Better quality but slower"
                )
                
                process_btn = gr.Button("🚀 Process Video", variant="primary", scale=2)
            
            with gr.Column(scale=1):
                gr.HTML("<h2>📊 Results</h2>")
                
                status_output = gr.Textbox(
                    label="📋 Status",
                    lines=8,
                    interactive=False,
                    value="🔄 Waiting for input..."
                )
        
        with gr.Row():
            with gr.Column():
                video_output = gr.Video(
                    label="🎥 Dubbed Video",
                    type="filepath"
                )
            
            with gr.Column():
                transcription_output = gr.Dataframe(
                    label="📝 Transcription & Translation",
                    interactive=False
                )
        
        gr.HTML("""
        <div style="margin-top: 30px; padding: 20px; background: #f0f0f0; border-radius: 10px;">
            <h3>💡 How to Use:</h3>
            <ol style="text-align: left;">
                <li>Paste a YouTube link or video URL</li>
                <li>Select source and target languages</li>
                <li>Choose Whisper model (base for speed, medium/large for quality)</li>
                <li>Click "🚀 Process Video" and wait</li>
                <li>Download the dubbed video + subtitles</li>
            </ol>
            <p style="color: #666; font-size: 14px;">
                ⏱️ <b>Processing time:</b> 15-45 minutes depending on video length<br>
                💾 <b>Storage needed:</b> ~3-5 GB for models<br>
                ⚡ <b>GPU recommended</b> for faster processing
            </p>
        </div>
        """)
        
        # Connect button
        process_btn.click(
            fn=process_video,
            inputs=[video_url, source_lang, target_lang, whisper_model],
            outputs=[status_output, video_output, transcription_output]
        )
    
    return demo

if __name__ == "__main__":
    print("\n✨ Starting DubSync Gradio Interface...\n")
    
    demo = create_interface()
    
    print("\n" + "="*60)
    print("🎉 DubSync Gradio is ready!")
    print("="*60)
    print("\n📱 Opening Gradio interface...\n")
    
    # Launch with Colab settings
    demo.launch(
        share=True,  # Create public link
        show_error=True,
        debug=False
    )
