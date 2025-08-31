import os
import subprocess

class AudioExtractor:
    """
    Extrai áudio de vídeos usando FFmpeg.
    """
    def __init__(self, progress_callback=None):
        self.progress_callback = progress_callback

    def _report(self, value):
        if self.progress_callback:
            try:
                self.progress_callback(int(value))
            except Exception:
                pass

    def extract_audio_fast(self, video_path, output_mp3):
        """Extrai o áudio do vídeo e salva em MP3."""
        if not video_path or not os.path.exists(video_path):
            return False, "Arquivo de vídeo não encontrado."

        out_dir = os.path.dirname(output_mp3) or "."
        os.makedirs(out_dir, exist_ok=True)

        self._report(5)
        cmd = [
            "ffmpeg", "-y",
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
                return False, f"Erro no FFmpeg: {proc.stderr.strip()}"
            self._report(100)
            return True, ""
        except FileNotFoundError:
            return False, "FFmpeg não encontrado. Coloque em ffmpeg/bin/ffmpeg.exe ou no PATH."
        except Exception as e:
            return False, str(e)
