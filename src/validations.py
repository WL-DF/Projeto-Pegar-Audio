import os
import subprocess

def validate_video_path(video_path):
    if not video_path:
        return False, "Caminho do vídeo não pode ser vazio."
    if not os.path.exists(video_path):
        return False, "Arquivo de vídeo não encontrado."
    if not video_path.lower().endswith(('.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv')):
        return False, "Formato não suportado. Use MP4, AVI, MKV, MOV, WMV ou FLV."
    return True, ""

def validate_output_dir(output_dir):
    if not output_dir:
        return False, "Diretório de saída inválido."
    if not os.path.isdir(output_dir):
        try:
            os.makedirs(output_dir, exist_ok=True)
        except Exception:
            return False, "Diretório de saída não existe e não pôde ser criado."
    if not os.access(output_dir, os.W_OK):
        return False, "Sem permissão para escrever no diretório."
    return True, ""

def validate_ffmpeg():
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            return False, result.stderr or result.stdout or "FFmpeg retornou código não-zero."
        if "libmp3lame" not in result.stdout and "lame" not in result.stdout:
            # nem sempre aparece; só advertência
            return True, "FFmpeg instalado, atenção: libmp3lame não encontrado (verifique codecs)."
        return True, ""
    except FileNotFoundError:
        # tenta localizar em ffmpeg/bin
        local = os.path.join("ffmpeg", "bin", "ffmpeg.exe")
        if os.path.exists(local):
            return True, ""
        return False, "FFmpeg não encontrado. Instale e coloque no PATH ou adicione ffmpeg/bin/ffmpeg.exe no projeto."
    except Exception as e:
        return False, f"Erro ao verificar FFmpeg: {e}"
