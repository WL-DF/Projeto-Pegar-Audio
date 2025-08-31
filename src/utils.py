import os
import subprocess

def get_output_paths(video_path, transcribe):
    """Gera os caminhos de saída baseados no caminho do vídeo."""
    output_dir = os.path.dirname(video_path)
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    output_mp3 = os.path.join(output_dir, f"{base_name}.mp3")
    output_txt = os.path.join(output_dir, f"{base_name}.txt") if transcribe else None
    
    return output_mp3, output_txt

def format_file_size(size_bytes):
    """Formata o tamanho do arquivo para uma string legível."""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
        
    return f"{size_bytes:.2f} {size_names[i]}"

def check_ffmpeg_installation():
    """Verifica se o FFmpeg está instalado corretamente."""
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        return result.returncode == 0, result.stdout if result.returncode == 0 else result.stderr
    except FileNotFoundError:
        return False, "FFmpeg não encontrado no PATH"