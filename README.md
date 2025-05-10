# Video/Audio Transcription Tool

A simple command-line tool for transcribing audio and video files using OpenAI's Whisper model.

## Features

- Supports various audio and video formats (MP3, WAV, MP4, etc.)
- Multiple model sizes available (tiny, base, small, medium, large)
- Runs completely offline
- Simple command-line interface
- Progress tracking during transcription

## Installation

1. Make sure you have Python 3.7+ installed
2. Install FFmpeg (required for audio processing):
   - Windows: Download from [FFmpeg website](https://ffmpeg.org/download.html)
   - Linux: `sudo apt install ffmpeg`
   - macOS: `brew install ffmpeg`

3. Install the required Python packages:
```bash
pip install -r requirements.txt
```

## Usage

Basic usage:
```bash
python transcriber.py path/to/your/file.mp3
```

Advanced options:
```bash
python transcriber.py path/to/your/file.mp3 --model medium --output transcription.txt
```

### Command-line Arguments

- `file_path`: Path to the audio/video file (required)
- `--model`: Whisper model to use (default: medium)
  - Options: tiny, base, small, medium, large
- `--output`: Path to save the transcription (optional)
  - If not specified, will use the input filename with "_transcription.txt" suffix

## Model Sizes

- `tiny`: Fastest, lowest accuracy
- `base`: Good balance of speed and accuracy
- `small`: Better accuracy, slower
- `medium`: High accuracy, slower
- `large`: Best accuracy, slowest

Choose the model based on your needs for speed vs. accuracy.

## Notes

- The first run will download the selected Whisper model (this only happens once)
- Transcription speed depends on your hardware (CPU/GPU)
- For best performance, use a GPU if available 
