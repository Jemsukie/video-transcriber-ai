import streamlit as st
import whisper
import tempfile
import os
from datetime import datetime
import subprocess

# Whisper model options
MODEL_OPTIONS = ["tiny", "base", "small", "medium", "large"]

def transcribe_audio(file_path, model_name, log_callback=None):
    try:
        if log_callback:
            log_callback(f"Loading Whisper model: {model_name}")
        model = whisper.load_model(model_name)
        if log_callback:
            log_callback(f"Transcribing file: {file_path}")
        result = model.transcribe(file_path)
        return result['text']
    except Exception as e:
        if log_callback:
            log_callback(f"Error: {str(e)}")
        return None

def convert_to_mp3(input_path, output_path, log_callback=None):
    try:
        if log_callback:
            log_callback(f"Converting {input_path} to mp3: {output_path}")
        cmd = [
            "ffmpeg", "-y", "-i", input_path,
            "-vn", "-acodec", "libmp3lame", "-ar", "44100", "-ac", "2", "-ab", "192k", "-f", "mp3", output_path
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if log_callback:
            log_callback(f"Conversion complete: {output_path}")
        return output_path
    except Exception as e:
        if log_callback:
            log_callback(f"ffmpeg conversion error: {str(e)}")
        return None

def main():
    st.title("🎤 Video/Audio Transcriber (Whisper)")
    st.write("Transcribe your audio or video files locally using OpenAI's Whisper model. No tokens or API keys required!")

    # File uploader
    uploaded_file = st.file_uploader("Choose an audio or video file", type=["mp3", "wav", "mp4", "m4a", "aac", "flac", "ogg", "webm"])

    # Model selection
    model_name = st.selectbox("Select Whisper model", MODEL_OPTIONS, index=3)

    # Log area
    st.subheader("Logs")
    log_area = st.empty()
    logs = []
    def log_callback(msg):
        logs.append(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")
        log_area.code("\n".join(logs), language="text")

    # Transcribe button
    if st.button("Transcribe"):
        if not uploaded_file:
            st.warning("Please upload a file first.")
        else:
            # Save uploaded file to a temp location
            with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
                tmp_file.write(uploaded_file.read())
                tmp_path = tmp_file.name
            log_callback(f"Saved uploaded file to {tmp_path}")
            # If not mp3, convert to mp3
            ext = os.path.splitext(tmp_path)[1].lower()
            if ext != ".mp3":
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as mp3_file:
                    mp3_path = mp3_file.name
                converted = convert_to_mp3(tmp_path, mp3_path, log_callback)
                if converted:
                    os.remove(tmp_path)
                    tmp_path = mp3_path
                    # Add download button for converted mp3
                    with open(tmp_path, "rb") as f:
                        st.download_button("Download Converted MP3", f, file_name="converted.mp3")
                else:
                    st.error("Failed to convert file to mp3. See logs above.")
                    os.remove(tmp_path)
                    return
            # Transcribe
            transcript = transcribe_audio(tmp_path, model_name, log_callback)
            if transcript:
                st.success("Transcription complete!")
                # Ensure output folder exists
                output_dir = os.path.join(os.getcwd(), "output")
                os.makedirs(output_dir, exist_ok=True)
                output_path = os.path.join(output_dir, "transcript.txt")
                with open(output_path, "w", encoding="utf-8") as f:
                    f.write(transcript)
                st.download_button("Download Transcript", transcript, file_name="transcript.txt")
                st.text_area("Transcript", transcript, height=300)
            else:
                st.error("Transcription failed. See logs above.")
            # Clean up temp file
            os.remove(tmp_path)

if __name__ == "__main__":
    main() 
