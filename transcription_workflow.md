# Audio/Video Transcription Workflow

## 1. File Picker
- Use a file picker (e.g., Streamlit or web UI) to allow users to upload their audio or video file.

## 2. File Type Detection & Conversion
- **If the uploaded file is a video:**
  - Convert it to `.mp3` using `ffmpeg`.
  - Example command:
    ```bash
    ffmpeg -i input_video.mp4 -vn -acodec libmp3lame -ar 44100 -ac 2 -ab 192k -f mp3 output_audio.mp3
    ```
- **If the uploaded file is audio but not `.mp3`:**
  - Convert it to `.mp3` using `ffmpeg`.
    ```bash
    ffmpeg -i input_audio.wav -acodec libmp3lame -ar 44100 -ac 2 -ab 192k -f mp3 output_audio.mp3
    ```
- **If the uploaded file is already `.mp3`:**
  - Proceed to chunking.

## 3. Chunking Audio into 100MB Files
- Use `ffmpeg` to split the `.mp3` file into 100MB chunks.
- Generate a unique group ID (e.g., with `uuid` in Python) for each upload session.
- Save all chunked audio files in a temporary/cache directory or an `output` folder for organization.
- Example command:
  ```bash
  ffmpeg -i output_audio.mp3 -f segment -segment_time 00:10:00 -c copy output/groupid_chunk%03d.mp3
  ```
  *(Note: Adjust `-segment_time` to approximate 100MB per chunk, as `ffmpeg` splits by time, not size. Use a script to calculate the correct time for 100MB chunks.)*

## 4. Transcription
- Transcribe each chunk separately using your transcription model (e.g., OpenAI Whisper).
- Save each chunk's transcript with a unique filename (e.g., `groupid_chunk001.txt`) in the `output` folder.

## 5. Merging Transcription Results
- Concatenate all chunk transcripts in order.
- Optionally, add chunk markers (e.g., `--- Chunk 1 ---`).
- Save the final merged transcript as a text file in the `output` folder.

## 6. Temporary Storage & Download
- Store all intermediate and final files in a temporary/cache directory (e.g., using Python's `tempfile` module).
- Move or save the final merged transcript output text file to an `output` folder for easier access and organization.
- Provide a download link for the merged transcript in the UI.
- Files are not stored permanently and will be deleted after the session or after a set period.

---

## Example Python Libraries
- `ffmpeg-python` or `subprocess` for running ffmpeg commands
- `uuid` for unique group IDs
- `tempfile` for temporary storage
- `streamlit` for UI (file picker, download link)

---

## Notes
- Ensure `ffmpeg` is installed and available in your system PATH.
- Adjust chunking logic as needed to ensure each chunk is close to 100MB.
- Clean up temporary files after download or session ends. 
