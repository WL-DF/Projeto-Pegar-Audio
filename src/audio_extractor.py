import os
import subprocess

class AudioExtractor:
    """
    Extrai áudio de vídeos usando FFmpeg.
    Interface:
      extractor = AudioExtractor(progress_callback=None)
      success, msg = extractor.extract_audio_fast(video_path, output_mp3)
    """
    def __init__(self, progress_callback=None):
        self.progress_callback = progress_callback

    def _report(self, value):
        try:
            if self.progress_callback:
                self.progress_callback(int(value))
        except Exception:
            pass

    def _find_ffmpeg_cmd(self):
        # Prioriza ffmpeg/bin/ffmpeg.exe no projeto (Windows) se existir
        local = os.path.join("ffmpeg", "bin", "ffmpeg.exe")
        if os.path.exists(local):
            return local
        # Fallback para comando global
        return "ffmpeg"

    def extract_audio_fast(self, video_path, output_mp3):
        """Extrai o áudio do vídeo e salva em MP3. Retorna (True,"") ou (False, "erro")."""
        if not video_path or not os.path.exists(video_path):
            return False, "Arquivo de vídeo não encontrado."

        out_dir = os.path.dirname(output_mp3) or "."
        try:
            os.makedirs(out_dir, exist_ok=True)
        except Exception as e:
            return False, f"Não foi possível criar diretório de saída: {e}"

        self._report(5)

        ffmpeg_cmd = self._find_ffmpeg_cmd()
        cmd = [
            ffmpeg_cmd, "-y",
            "-i", video_path,
            "-vn",
            "-ar", "44100",
            "-ac", "2",
            "-b:a", "192k",
            output_mp3
        ]

        try:
            proc = subprocess.run(cmd, capture_output=True, text=True)
            if proc.returncode != 0:
                stderr = proc.stderr or proc.stdout or "Erro desconhecido do FFmpeg."
                return False, f"FFmpeg falhou: {stderr.strip()}"
            # basic sanity: output file exists and >1KB
            if not os.path.exists(output_mp3) or os.path.getsize(output_mp3) < 1024:
                return False, "Arquivo de áudio gerado é inválido (muito pequeno)."
            self._report(60)
            self._report(100)
            return True, ""
        except FileNotFoundError:
            return False, "FFmpeg não encontrado. Coloque em ffmpeg/bin/ffmpeg.exe ou instale no PATH."
        except Exception as e:
            return False, f"Erro ao executar FFmpeg: {str(e)}"
