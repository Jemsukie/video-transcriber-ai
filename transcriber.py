import whisper
import argparse
import os
from tqdm import tqdm

def transcribe_file(file_path, model_name="medium"):
    """
    Transcribe an audio or video file using Whisper.
    
    Args:
        file_path (str): Path to the audio/video file
        model_name (str): Whisper model to use (tiny, base, small, medium, large)
    
    Returns:
        dict: Transcription result containing text and segments
    """
    try:
        # Load the Whisper model
        print(f"Loading Whisper model: {model_name}")
        model = whisper.load_model(model_name)
        
        # Transcribe the file
        print(f"Transcribing file: {file_path}")
        result = model.transcribe(file_path)
        
        return result
    except Exception as e:
        print(f"Error during transcription: {str(e)}")
        return None

def save_transcription(result, output_path):
    """
    Save the transcription to a text file.
    
    Args:
        result (dict): Transcription result from Whisper
        output_path (str): Path to save the transcription
    """
    if result is None:
        return
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result['text'])
        print(f"Transcription saved to: {output_path}")
    except Exception as e:
        print(f"Error saving transcription: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Transcribe audio/video files using Whisper')
    parser.add_argument('file_path', help='Path to the audio/video file')
    parser.add_argument('--model', default='medium', choices=['tiny', 'base', 'small', 'medium', 'large'],
                      help='Whisper model to use (default: medium)')
    parser.add_argument('--output', help='Output file path for the transcription')
    
    args = parser.parse_args()
    
    # Validate input file
    if not os.path.exists(args.file_path):
        print(f"Error: File not found: {args.file_path}")
        return
    
    # Set default output path if not provided
    if not args.output:
        base_name = os.path.splitext(os.path.basename(args.file_path))[0]
        output_dir = os.path.join(os.getcwd(), "output")
        os.makedirs(output_dir, exist_ok=True)
        args.output = os.path.join(output_dir, f"{base_name}_transcription.txt")
    
    # Transcribe the file
    result = transcribe_file(args.file_path, args.model)
    
    if result:
        save_transcription(result, args.output)

if __name__ == "__main__":
    main() 
