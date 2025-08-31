# utils.py
import os
from pathlib import Path

def get_output_paths(video_path, transcribe):
    output_dir = os.path.dirname(video_path) or "."
    base = os.path.splitext(os.path.basename(video_path))[0]
    output_mp3 = os.path.join(output_dir, f"{base}.mp3")
    output_srt = os.path.join(output_dir, f"{base}.srt") if transcribe else None
    return output_mp3, output_srt

def format_file_size(size_bytes):
    if not size_bytes:
        return "0B"
    units = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    size = float(size_bytes)
    while size >= 1024 and i < len(units)-1:
        size /= 1024.0
        i += 1
    return f"{size:.2f} {units[i]}"

def find_ffmpeg():
    local = Path("ffmpeg/bin/ffmpeg.exe")
    if local.exists():
        return str(local)
    return "ffmpeg"