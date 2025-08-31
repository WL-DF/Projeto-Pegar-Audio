import os
import subprocess

def validate_video_path(video_path):
    """Valida se o caminho do vídeo é válido e suportado."""
    if not video_path:
        return False, "Caminho do vídeo não pode ser vazio."
    if not os.path.exists(video_path):
        return False, "Arquivo de vídeo não encontrado."
    if not video_path.lower().endswith(('.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv')):
        return False, "Formato não suportado. Use MP4, AVI, MKV, MOV, WMV ou FLV."
    return True, ""

def validate_output_dir(output_dir):
    """Valida se o diretório de saída é acessível."""
    if not os.path.isdir(output_dir):
        return False, "Diretório de saída inválido."
    if not os.access(output_dir, os.W_OK):
        return False, "Sem permissão para escrever no diretório."
    return True, ""

def validate_ffmpeg():
    """Valida se o FFmpeg está instalado e acessível."""
    try:
        result = subprocess.run(['ffmpeg', '-version'], check=True, capture_output=True, text=True, timeout=10)
        
        # Verifica se o codec MP3 está disponível
        if "libmp3lame" not in result.stdout:
            return False, "FFmpeg não possui suporte a MP3 (libmp3lame)."
            
        return True, ""
    except subprocess.TimeoutExpired:
        return False, "FFmpeg não respondeu. Pode estar corrompido ou mal instalado."
    except FileNotFoundError:
        return False, "FFmpeg não encontrado no PATH. Instale o FFmpeg e adicione ao PATH."
    except Exception as e:
        return False, f"Erro ao validar FFmpeg: {str(e)}"