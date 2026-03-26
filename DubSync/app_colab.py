"""
DubSync - Google Colab Version (No API Required)
This version uses only local models, no external APIs needed.
Compatible with Google Colab GPU
"""

import os
import sys

# Set environment variables for writable paths (Colab compatible)
os.environ["XDG_CONFIG_HOME"] = "/tmp/.config"
os.environ["XDG_CACHE_HOME"] = "/tmp/.cache"
os.environ["HF_HOME"] = "/tmp/huggingface"
os.environ["HF_HUB_CACHE"] = "/tmp/huggingface/hub"
os.environ["TRANSFORMERS_CACHE"] = "/tmp/transformers"
os.environ["TORCH_HOME"] = "/tmp/torch"
os.environ["MPLCONFIGDIR"] = "/tmp/matplotlib"
os.environ["STREAMLIT_HOME"] = "/tmp/.streamlit"

# Make sure directories exist
for path in [
    os.environ["XDG_CONFIG_HOME"],
    os.environ["XDG_CACHE_HOME"],
    os.environ["HF_HOME"],
    os.environ["HF_HUB_CACHE"],
    os.environ["TRANSFORMERS_CACHE"],
    os.environ["TORCH_HOME"],
    os.environ["MPLCONFIGDIR"],
    os.environ["STREAMLIT_HOME"],
]:
    os.makedirs(path, exist_ok=True)

import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from moviepy import VideoFileClip, AudioFileClip, CompositeAudioClip
import whisper
from pydub import AudioSegment
import shutil
import yt_dlp
import ast
import time
import torch
import pandas as pd
import streamlit as st
import json
import numpy as np
import librosa
from scipy.signal import butter, filtfilt

# Import local translation and LLM libraries
from transformers import pipeline, MarianMTModel, MarianTokenizer
import warnings
warnings.filterwarnings('ignore')

print("Streamlit config dir:", os.environ.get("STREAMLIT_CONFIG_DIR"))

device = "cuda" if torch.cuda.is_available() else "cpu"

st.set_page_config(page_title=f"DubSync Colab ({device})", layout="wide")

os.makedirs(os.environ["XDG_CACHE_HOME"], exist_ok=True)
temp_folder = os.path.join("/tmp", "resources")
demo_dir = "demos"
sample_output_dir = os.path.join(temp_folder, "sample_outputs")
cropped_audio_dir = os.path.join(temp_folder, "cropped_audio")
cloned_audio_dir = os.path.join(temp_folder, "cloned_audio")
os.makedirs(temp_folder, exist_ok=True)
os.makedirs(cropped_audio_dir, exist_ok=True)
os.makedirs(cloned_audio_dir, exist_ok=True)
os.makedirs(sample_output_dir, exist_ok=True)

# Global variable to cache translation models
_translation_model_cache = {}

def get_translation_model(model_name):
    """
    Load and cache translation model to avoid reloading
    Uses Helsinki-NLP Opus MT models
    """
    if model_name not in _translation_model_cache:
        try:
            tokenizer = MarianTokenizer.from_pretrained(model_name)
            model = MarianMTModel.from_pretrained(model_name).to(device)
            _translation_model_cache[model_name] = (model, tokenizer)
        except Exception as e:
            st.warning(f"Could not load model {model_name}: {e}")
            return None, None
    
    return _translation_model_cache[model_name]

def translate_text_local(texts, source_lang_code, target_lang_code):
    """
    Translate text using local Helsinki-NLP models
    Supports: ja->en, en->zh, zh->en, etc.
    """
    # Map language codes to model names
    # Format: Helsinki-NLP/Opus-MT-{source}-{target}
    model_name = f"Helsinki-NLP/Opus-MT-{source_lang_code}-{target_lang_code}"
    
    try:
        model, tokenizer = get_translation_model(model_name)
        if model is None:
            st.warning(f"Translation model not available for {source_lang_code}->{target_lang_code}")
            return texts  # Return original if translation fails
        
        # Batch translate
        inputs = tokenizer(texts, return_tensors="pt", padding=True).to(device)
        with torch.no_grad():
            outputs = model.generate(**inputs)
        
        translated = tokenizer.batch_decode(outputs, skip_special_tokens=True)
        return translated
    except Exception as e:
        st.warning(f"Translation error: {e}. Returning original text.")
        return texts

def enhance_translation_with_local_llm(segments, source_lang, target_lang):
    """
    Use a lightweight local LLM to enhance translation quality
    Falls back to simple enhancement if model not available
    """
    try:
        # Try to use a lightweight instruction model
        # Using a smaller model that can run on Colab
        pipe = pipeline(
            "text2text-generation",
            model="google/flan-t5-base",  # Small, fast model
            device=0 if device == "cuda" else -1
        )
        
        enhanced_segments = []
        for segment in segments:
            if "translation" not in segment or not segment["translation"]:
                enhanced_segments.append(segment)
                continue
            
            prompt = f"""Make this translation sound natural and expressive for dubbing:
Original: {segment['text']}
Translation: {segment['translation']}
Language: {target_lang}

Provide only the enhanced translation:"""
            
            try:
                result = pipe(prompt, max_length=100, do_sample=False)
                enhanced_text = result[0]['generated_text'].strip()
                segment["translation"] = enhanced_text
            except:
                pass  # Keep original translation if enhancement fails
            
            enhanced_segments.append(segment)
        
        return enhanced_segments
    except Exception as e:
        print(f"Local LLM enhancement not available: {e}")
        return segments

def translate_with_local_models(segments, source_lang_code, target_lang_code, source_lang_name, target_lang_name):
    """
    Translate segments using local models without API
    """
    with st.spinner(f"🌐 Translating to {target_lang_name}..."):
        try:
            # Extract texts for translation
            texts_to_translate = [seg["text"] for seg in segments]
            
            # Translate using local model
            translated_texts = translate_text_local(texts_to_translate, source_lang_code, target_lang_code)
            
            # Add translations to segments
            for i, segment in enumerate(segments):
                if i < len(translated_texts):
                    segment["translation"] = translated_texts[i]
                else:
                    segment["translation"] = segment["text"]
            
            # Try to enhance with local LLM for better quality
            # segments = enhance_translation_with_local_llm(segments, source_lang_name, target_lang_name)
            
            print(f"[Colab] Translation completed", flush=True)
            return segments
            
        except Exception as e:
            st.error(f"Translation failed: {e}")
            print(f"Translation error: {e}", flush=True)
            # Fallback: use original text as translation
            for segment in segments:
                segment["translation"] = segment["text"]
            return segments

def clean_up():
    shutil.rmtree(temp_folder)
    st.session_state.is_processing = False

def extract_audio_from_video(video_path):
    with st.spinner("🎬 Extracting audio from the video..."):
        try:
            video = VideoFileClip(video_path)
            audio_path = os.path.join(temp_folder, "extracted_audio.wav")
            video.audio.write_audiofile(audio_path, verbose=False, logger=None)
            return audio_path
        except Exception as e:
            st.error(f"Failed to extract audio: {e}")
            clean_up()
            sys.exit(1)
            return None

def separate_audio_layers(audio_path):
    with st.spinner("🎶 Separating audio layers..."):
        output_dir = os.path.join(temp_folder, "demucs_output")
        subprocess.run(["demucs", "-o", output_dir,
                       f"--device={device}", audio_path], capture_output=True, text=True)
        print(output_dir)
        return output_dir

def is_model_cached(model_name):
    cache_dir = os.path.expanduser("~/.cache/whisper")
    model_files = [f"{model_name}.pt"]
    return all(os.path.exists(os.path.join(cache_dir, f)) for f in model_files)

def transcribe_audio(audio_path, selected_model, input_language_value):
    """Transcribe audio using local Whisper model"""
    if not is_model_cached(selected_model):
        message = f"Model {selected_model} not found in cache. It will be downloaded."
    else:
        message = f"Model {selected_model} is already cached. Transcribing vocals..."
    
    with st.spinner(message):
        model = whisper.load_model(selected_model, device=device)
        result = model.transcribe(
            audio_path, language=input_language_value, word_timestamps=False, fp16=False, condition_on_previous_text=True)
        return result["segments"]

def generate_audio_from_segments(segments, original_audio_path):
    with st.spinner("🌍 Generating audio from segments..."):
        translated_audio = os.path.join(temp_folder, "translated_audio.wav")
        final_audio = AudioSegment.silent(duration=0)
        last_end_time = 0
        for idx, segment in enumerate(segments):
            start_ms = segment["start"]*1000
            end_ms = segment["end"]*1000
            duration_ms = (end_ms - start_ms)

            audio_segment_path = os.path.join(cloned_audio_dir, f"output_{idx}.wav")
            if not os.path.exists(audio_segment_path):
                # Create silent segment if output doesn't exist
                spoken = AudioSegment.silent(duration=int(duration_ms))
            else:
                spoken = AudioSegment.from_file(audio_segment_path)

            # Add silence before this segment if needed
            gap_duration = start_ms - int(last_end_time * 1000)
            if gap_duration > 0:
                original_audio = AudioSegment.from_file(original_audio_path)
                gap_start = int(last_end_time * 1000)
                gap_end = int(start_ms)
                gap_audio = original_audio[gap_start:gap_end]
                final_audio += gap_audio

            # Clip or pad the TTS output to exactly fit segment duration
            if len(spoken) > duration_ms:
                spoken = spoken[:int(duration_ms)]
            else:
                spoken += AudioSegment.silent(duration=int(duration_ms - len(spoken)))

            final_audio += spoken
            last_end_time = segment["end"]
            print(f"Segment {idx+1}/{len(segments)} | {segment['start']}", flush=True)
        
        final_audio.export(translated_audio, format="wav")
        return translated_audio

def run_f5_tts_infer(model, ref_audio, ref_text, gen_text, output_dir=None, output_file=None):
    """Run F5-TTS voice cloning"""
    command = [
        "f5-tts_infer-cli",
        "--model", model,
        "--ref_audio", ref_audio,
        "--ref_text", ref_text,
        "--gen_text", gen_text,
        "--speed", "0.8"
    ]
    if output_file:
        command += ["--output_file", output_file]
    if output_dir:
        command += ["--output_dir", output_dir]
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print("F5-TTS output:", result.stdout, flush=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print("F5-TTS Error:", e.stderr, flush=True)
        return None

def list_all_nested_contents(base_path):
    print(f"📂 Listing all folders and files in: {base_path}\n")
    for root, dirs, files in os.walk(base_path):
        level = root.replace(base_path, "").count(os.sep)
        indent = "  " * level
        folder_name = os.path.basename(root)
        print(f"{indent}📁 {folder_name}", flush=True)
        sub_indent = "  " * (level + 1)
        for f in files:
            print(f"{sub_indent}📄 {f}", flush=True)

def voice_cloning(segments, audio_path, max_threads=2):
    """Clone voice using F5-TTS"""
    audio = AudioSegment.from_file(audio_path)
    with st.spinner("🔊 Cropping audio segments..."):
        for segment in segments:
            start_ms = int(segment["start"] * 1000)
            end_ms = int(segment["end"] * 1000)
            cropped = audio[start_ms:end_ms]
            cropped.export(os.path.join(cropped_audio_dir, f"cropped_{segment['id']}.wav"), format="wav")
            print(f"cropped_{segment['id']}.wav", flush=True)
    
    with st.spinner("🤖 Cloning voice..."):
        try:
            print("[Voice Cloning] - Initiated", flush=True)
            for segment in segments:
                ref_audio = os.path.join(cropped_audio_dir, f"cropped_{segment['id']}.wav")
                ref_text = segment["text"]
                gen_text = segment.get("translation", segment["text"])
                
                if not ref_text or not gen_text:
                    print(f"Skipping segment {segment['id']} due to empty text")
                    continue
                
                run_f5_tts_infer(
                    "F5TTS_v1_Base",
                    ref_audio,
                    ref_text,
                    gen_text,
                    output_dir=cloned_audio_dir,
                    output_file=f"output_{segment['id']}.wav"
                )
            print("[Done] Voice cloning", flush=True)
        except Exception as e:
            print(f"Voice cloning failed: {e}")
            st.error(f"Voice cloning failed: {e}")

def set_processing(value=True):
    st.session_state.is_processing = value

def generate_srt_subtitles(segments, output_path, subtitle_type="translation"):
    """Generate SRT subtitle file from segments"""
    try:
        with open(output_path, 'w', encoding='utf-8') as srt_file:
            for i, segment in enumerate(segments, 1):
                start_time = segment["start"]
                end_time = segment["end"]
                start_srt = seconds_to_srt_time(start_time)
                end_srt = seconds_to_srt_time(end_time)

                if subtitle_type == "translation" and "translation" in segment:
                    text = segment["translation"]
                elif "text" in segment:
                    text = segment["text"]
                else:
                    text = "..."

                text = text.replace('\n', ' ').strip()
                if not text:
                    continue

                srt_file.write(f"{i}\n")
                srt_file.write(f"{start_srt} --> {end_srt}\n")
                srt_file.write(f"{text}\n\n")

        return output_path
    except Exception as e:
        st.error(f"Failed to generate subtitles: {e}")
        return None

def seconds_to_srt_time(seconds):
    """Convert seconds to SRT time format (HH:MM:SS,mmm)"""
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{secs:02d},{milliseconds:03d}"

def load_demo_data():
    """Load demo data from demo.json file"""
    demo_json_path = os.path.join(demo_dir, "demo.json")
    try:
        with open(demo_json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"Demo file not found: {demo_json_path}")
        return []
    except json.JSONDecodeError as e:
        st.error(f"Error reading demo file: {e}")
        return []

def clean_audio_for_transcription(audio_path, output_path=None, noise_reduction_strength=0.8, enable_cleaning=True):
    """Clean and preprocess audio for better Whisper transcription"""
    if not enable_cleaning:
        return audio_path
    
    with st.spinner("🧹 Cleaning audio for better transcription..."):
        try:
            audio_data, sample_rate = librosa.load(audio_path, sr=16000)
            
            # Noise reduction
            noise_sample_duration = min(1.0, len(audio_data) / sample_rate * 0.1)
            noise_sample_size = int(noise_sample_duration * sample_rate)
            
            if len(audio_data) > noise_sample_size:
                try:
                    import noisereduce as nr
                    audio_data = nr.reduce_noise(
                        y=audio_data,
                        sr=sample_rate,
                        stationary=False,
                        prop_decrease=noise_reduction_strength
                    )
                except ImportError:
                    # Fallback: High-pass filter
                    nyquist = sample_rate * 0.5
                    low_cutoff = 80
                    low_cutoff_normalized = low_cutoff / nyquist
                    b, a = butter(5, low_cutoff_normalized, btype='high')
                    audio_data = filtfilt(b, a, audio_data)
                    print("Using high-pass filter for noise reduction")
            
            # Normalize audio levels
            rms = np.sqrt(np.mean(audio_data**2))
            if rms > 0:
                target_rms = 10**(-20/20)
                audio_data = audio_data * (target_rms / rms)
            
            # Remove silence
            intervals = librosa.effects.split(audio_data, top_db=30, frame_length=2048, hop_length=512)
            
            # Apply gentle compression
            threshold = 0.95
            audio_data = np.where(
                np.abs(audio_data) > threshold,
                np.sign(audio_data) * (threshold + (np.abs(audio_data) - threshold) * 0.1),
                audio_data
            )
            
            # Final normalization
            max_amplitude = np.max(np.abs(audio_data))
            if max_amplitude > 0.95:
                audio_data = audio_data * (0.95 / max_amplitude)
            
            if output_path is None:
                output_path = audio_path.replace('.wav', '_cleaned.wav')
            
            audio_int16 = (audio_data * 32767).astype(np.int16)
            cleaned_audio = AudioSegment(
                audio_int16.tobytes(),
                frame_rate=sample_rate,
                sample_width=2,
                channels=1
            )
            
            cleaned_audio.export(output_path, format="wav")
            print(f"Audio cleaned and saved to: {output_path}")
            return output_path
        except Exception as e:
            st.warning(f"Audio cleaning failed, using original audio: {e}")
            return audio_path

def analyze_audio_quality(audio_path, label="Audio"):
    """Analyze audio quality metrics"""
    try:
        audio_data, sample_rate = librosa.load(audio_path, sr=None)
        
        rms = np.sqrt(np.mean(audio_data**2))
        peak = np.max(np.abs(audio_data))
        snr_estimate = 20 * np.log10(rms / (np.std(audio_data) + 1e-10))
        dynamic_range = 20 * np.log10(peak / (rms + 1e-10))
        
        metrics = {
            "Sample Rate": f"{sample_rate} Hz",
            "Duration": f"{len(audio_data) / sample_rate:.2f} seconds",
            "RMS Level": f"{20 * np.log10(rms + 1e-10):.2f} dB",
            "Peak Level": f"{20 * np.log10(peak + 1e-10):.2f} dB",
            "Estimated SNR": f"{snr_estimate:.2f} dB",
            "Dynamic Range": f"{dynamic_range:.2f} dB"
        }
        
        st.write(f"**{label} Quality Metrics:**")
        for metric, value in metrics.items():
            st.write(f"- {metric}: {value}")
        
        return metrics
    except Exception as e:
        st.warning(f"Could not analyze audio quality: {e}")
        return {}

# Main Streamlit app
if __name__ == "__main__":
    if "is_processing" not in st.session_state:
        st.session_state.is_processing = False

    with st.sidebar:
        st.write("🌍 Language Options")
        input_languages = [
            ("Japanese", "ja"), ("English", "en"), ("Chinese", "zh"),
            ("Korean", "ko"), ("Spanish", "es"), ("French", "fr"),
            ("German", "de"), ("Italian", "it"), ("Portuguese", "pt"),
            ("Russian", "ru"), ("Arabic", "ar"), ("Hindi", "hi")
        ]
        output_languages = [("English", "en"), ("Chinese", "zh"), ("Hindi", "hi")]

        input_language_label = st.selectbox(
            "Select the language of the original video",
            options=[label for label, value in input_languages],
            index=0,
            disabled=st.session_state.is_processing,
        )
        input_language_value = dict(input_languages)[input_language_label]
        
        st.write("Output Language")
        output_language_label = st.selectbox(
            "Select the language of the dubbed video",
            options=[label for label, value in output_languages],
            index=0,
            disabled=st.session_state.is_processing,
        )
        output_language_value = dict(output_languages)[output_language_label]
        
        st.divider()
        st.write("🎬 Video Input Options")
        
        video_file = None
        if video_file is not None:
            save_path = os.path.join("/tmp", video_file.name)
            with open(save_path, "wb") as f:
                f.write(video_file.read())
            st.video(save_path)
            st.success(f"Saved and loaded video from: {save_path}")
        
        video_url = st.text_input(
            "Enter the URL of a MP4 video (YouTube, etc.)",
            disabled=st.session_state.is_processing,
            on_change=set_processing,
            args=(True,)
        )
        
        st.divider()
        st.write("🎤 Transcription Options")
        whisper_models = ["tiny", "base", "small", "medium", "large", "large-v2", "large-v3", "turbo"]
        selected_model = st.selectbox(
            "Select Whisper model for transcription",
            options=whisper_models,
            index=3,  # Default to 'medium' for balance
            disabled=st.session_state.is_processing,
            help="Larger models provide better accuracy but are slower."
        )
        
        st.divider()
        st.write("🔊 Audio Enhancement Options")
        enable_audio_cleaning = st.checkbox(
            "Enable advanced audio cleaning",
            value=True,
            disabled=st.session_state.is_processing,
            help="Applies noise reduction, normalization, and other enhancements"
        )
        
        if enable_audio_cleaning:
            noise_reduction_strength = st.slider(
                "Noise reduction strength",
                min_value=0.1,
                max_value=1.0,
                value=0.8,
                step=0.1,
                disabled=st.session_state.is_processing,
                help="Higher values remove more noise but may affect speech quality"
            )
        
        st.divider()
        st.info(f"🖥️ Using device: **{device.upper()}**" +
                (" (GPU acceleration enabled)" if device == "cuda" else " (CPU only)"))
        
        st.markdown("---")
        st.markdown("**🚀 DubSync Colab Edition**\nNo API keys needed!\nAll models run locally.")

    if video_url:
        if "youtube.com" in video_url or "youtu.be" in video_url:
            with st.spinner("📥 Downloading video from URL..."):
                try:
                    ydl_opts = {
                        'format': 'bestvideo+bestaudio/best',
                        'outtmpl': os.path.join(temp_folder, "uploaded_video"),
                        'merge_output_format': 'mp4',
                        'quiet': True,
                    }
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(video_url, download=True)
                        video_file = ydl.prepare_filename(info)
                    st.success(f"✅ Downloaded: {info.get('title', 'Video')}")
                except Exception as e:
                    st.error(f"❌ Download error: {e}")

        else:
            try:
                with st.spinner("📥 Downloading video from URL..."):
                    import requests
                    response = requests.get(video_url, stream=True, timeout=30)
                    if response.status_code == 200:
                        uploaded_video_path = os.path.join(temp_folder, "uploaded_video.mp4")
                        with open(uploaded_video_path, "wb") as f:
                            for chunk in response.iter_content(chunk_size=8192):
                                if chunk:
                                    f.write(chunk)
                        video_file = open(uploaded_video_path, "rb")
                        st.success("✅ Video downloaded successfully!")
                    else:
                        st.error("❌ Failed to download video. Check the URL.")
            except Exception as e:
                st.error(f"❌ Download error: {e}")

    if video_file is not None:
        st.session_state.is_processing = True
        start_time = time.time()
        input_video_col, output_video_col = st.columns(2)
        st.divider()
        
        with input_video_col:
            st.subheader("📹 Input Video")
            st.video(video_file, muted=False)
        
        uploaded_video_path = os.path.join(temp_folder, "uploaded_video.mp4")
        if not os.path.exists(uploaded_video_path):
            with open(uploaded_video_path, "wb") as f:
                f.write(video_file.read())

        # Extract audio from video
        audio_path = extract_audio_from_video(uploaded_video_path)
        
        # Clean audio if enabled
        if enable_audio_cleaning:
            audio_path = clean_audio_for_transcription(
                audio_path,
                noise_reduction_strength=noise_reduction_strength if 'noise_reduction_strength' in locals() else 0.8
            )

        # Separate audio layers
        with output_video_col:
            output_dir = separate_audio_layers(audio_path)

        # Get vocals path
        separated_dir = os.path.join(
            output_dir, "htdemucs", os.path.splitext(os.path.basename(audio_path))[0])
        vocals_path = os.path.join(separated_dir, "vocals.wav")
        bg_music_path = os.path.join(separated_dir, "other.wav")
        bass_path = os.path.join(separated_dir, "bass.wav")
        drums_path = os.path.join(separated_dir, "drums.wav")

        # Transcribe audio
        with output_video_col:
            segments = transcribe_audio(vocals_path, selected_model, input_language_value)

        # Translate segments using local models (no API!)
        with output_video_col:
            segments = translate_with_local_models(
                segments,
                input_language_value,
                output_language_value,
                input_language_label,
                output_language_label
            )

        # Display transcription
        filtered_segments = [
            {
                "id": s.get("id"),
                "start (sec)": s.get("start"),
                "end (sec)": s.get("end"),
                "original": s.get("text"),
                "translation": s.get("translation", s.get("text")),
                "confidence": s.get('no_speech_prob', 0),
            }
            for s in segments
        ]
        
        df = pd.DataFrame(filtered_segments)
        st.subheader("📊 Transcription & Translation")
        st.data_editor(df, use_container_width=True, hide_index=True, num_rows="dynamic", disabled=True)
        
        segments_csv_path = os.path.join(
            sample_output_dir, f"output_segments_{selected_model}_{output_language_value}.csv")
        df.to_csv(segments_csv_path, index=False, encoding="utf-8")

        # Voice cloning
        with output_video_col:
            voice_cloning(segments, vocals_path)

        # Generate final dubbed audio
        translated_audio = generate_audio_from_segments(segments, audio_path)
        
        # Create dubbed video
        video = VideoFileClip(uploaded_video_path)
        translated_audio_clip = AudioFileClip(translated_audio)
        bg_audio = AudioFileClip(bg_music_path)
        drums_audio = AudioFileClip(drums_path)
        bass_audio = AudioFileClip(bass_path)
        
        with output_video_col:
            with st.spinner("🎬 Generating dubbed video..."):
                combined_audio = CompositeAudioClip(
                    [translated_audio_clip, bg_audio, drums_audio, bass_audio])
                video = video.with_audio(combined_audio)
                
                dubbed_video_path = os.path.join(
                    sample_output_dir, f"dubbed_{selected_model}_{output_language_value}.mp4")
                subtitle_path = os.path.join(
                    sample_output_dir, f"dubbed_{selected_model}_{output_language_value}.srt")
                
                generate_srt_subtitles(segments, subtitle_path)
                video.write_videofile(
                    dubbed_video_path,
                    codec="libx264",
                    audio_codec="aac",
                    temp_audiofile=os.path.join(sample_output_dir, "temp-audio.m4a"),
                    remove_temp=True,
                    verbose=False,
                    logger=None
                )
                
                st.subheader("✨ Dubbed Video")
                st.video(dubbed_video_path, subtitles=subtitle_path)

        end_time = time.time()
        elapsed_time = end_time - start_time
        elapsed_minutes = round(elapsed_time / 60, 2)
        
        st.success(f"✅ Processing completed in {elapsed_minutes} minutes!")
        
        # Download buttons
        col1, col2 = st.columns(2)
        with col1:
            with open(dubbed_video_path, "rb") as f:
                st.download_button(
                    "📥 Download Dubbed Video",
                    f,
                    file_name=f"dubbed_{output_language_value}.mp4",
                    mime="video/mp4"
                )
        
        with col2:
            with open(segments_csv_path, "rb") as f:
                st.download_button(
                    "📥 Download Transcription CSV",
                    f,
                    file_name=f"transcription_{output_language_value}.csv",
                    mime="text/csv"
                )
        
        video_file = None
        clean_up()
    
    else:
        st.title("🎬 DubSync - Colab Edition (No API!)")
        st.markdown("""
        ## Welcome to DubSync - AI-Powered Video Dubbing
        
        Transform your videos with AI-powered dubbing that preserves voice characteristics and emotions.
        
        ### ✨ Features:
        - 🎤 **Voice Cloning** - Clone voices using F5-TTS
        - 🌐 **Translation** - Translate using local models (no API!)
        - 🎵 **Audio Separation** - Separate vocals, drums, bass, music
        - 🎬 **Video Dubbing** - Generate synchronized dubbed videos
        - 📊 **Transcription** - Powerful OpenAI Whisper models
        
        ### 🚀 How to Use:
        1. Enter a YouTube link or upload a video
        2. Select source and target languages
        3. Choose Whisper model size
        4. Click Process and wait for dubbing!
        
        ### 💡 Colab Tips:
        - Use **GPU Runtime** for faster processing
        - Smaller models (tiny, base) for quick tests
        - Larger models (large-v3) for best quality
        
        ### ⚙️ Tech Stack:
        - **Transcription**: OpenAI Whisper
        - **Translation**: Helsinki-NLP Opus-MT (Local)
        - **Voice Cloning**: F5-TTS
        - **Audio Separation**: Demucs
        - **Video Processing**: MoviePy
        
        ---
        **Ready to dub? Enter a video URL or upload a file above!**
        """)

print("\n✅ DubSync Colab Edition Loaded Successfully!\n")
