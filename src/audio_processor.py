# audio_processor.py
import os
import threading
from audio_extractor import AudioExtractor
from transcriber import Transcriber
from validations import validate_video_path, validate_output_dir
from progress_manager import ProgressManager
from utils import get_output_paths, format_file_size

class AudioProcessor:
    """Classe para orquestrar extração e transcrição."""

    def __init__(self, config=None):
        self.config = config
        self.is_processing = False
        self.progress_manager = ProgressManager(self._set_progress)
        self.extractor = AudioExtractor(self._set_progress)
        self.transcriber = Transcriber(self._set_progress)

    def _set_progress(self, value):
        if self.config and hasattr(self.config, "update_progress"):
            try:
                self.config.update_progress(value)
            except Exception:
                pass

    def process_video(self, video_path, transcribe=True, delete_mp3=False):
        """Processa o vídeo (validações, extrai e opcionalmente transcreve)."""
        if self.is_processing:
            if self.config:
                self.config.show_error("Já existe um processamento em andamento.")
            return

        if not video_path:
            if self.config:
                self.config.show_error("Selecione um vídeo primeiro.")
                self.config.status_label.config(text="", foreground="blue")  # Limpa status
            return

        is_valid, msg = validate_video_path(video_path)
        if not is_valid:
            if self.config:
                self.config.show_error(msg)
                self.config.status_label.config(text="", foreground="blue")
            return

        output_dir = os.path.dirname(video_path)
        is_valid, msg = validate_output_dir(output_dir)
        if not is_valid:
            if self.config:
                self.config.show_error(msg)
                self.config.status_label.config(text="", foreground="blue")
            return

        output_mp3, output_txt = get_output_paths(video_path, transcribe)

        # Se chegou aqui, validações ok: desabilita botão e inicia thread
        if self.config:
            self.config.disable_button()

        def task():
            self.is_processing = True
            try:
                if self.config:
                    self.config.status_label.config(text="Extraindo áudio...", foreground="blue")
                    self.config.update_progress(0)
                self.progress_manager.reset()

                ok, msg = self.extractor.extract_audio_fast(video_path, output_mp3)
                if not ok:
                    if self.config:
                        self.config.show_error(f"Erro ao extrair áudio: {msg}")
                    return

                if not transcribe:
                    if self.config:
                        self.config.update_progress(100)
                        self.config.status_label.config(text="Concluído (MP3 gerado)", foreground="green")
                        try:
                            size = os.path.getsize(output_mp3)
                            self.config.show_info(f"Arquivo gerado: {os.path.basename(output_mp3)} ({format_file_size(size)})")
                        except:
                            self.config.show_info("Arquivo MP3 gerado com sucesso.")
                    return

                # transcrição
                if self.config:
                    self.config.status_label.config(text="Transcrevendo áudio...", foreground="blue")
                ok, msg = self.transcriber.transcribe_audio(output_mp3, output_txt)
                if not ok:
                    if self.config:
                        self.config.show_error(f"Erro na transcrição: {msg}")
                    return

                # Se delete_mp3 ativado e transcrição ok, deleta MP3
                if delete_mp3 and ok:
                    try:
                        os.remove(output_mp3)
                    except Exception as e:
                        if self.config:
                            self.config.show_error(f"Erro ao deletar MP3: {e}")

                # sucesso
                if self.config:
                    mp3_size = os.path.getsize(output_mp3) if os.path.exists(output_mp3) else 0
                    txt_size = os.path.getsize(output_txt) if os.path.exists(output_txt) else 0
                    self.config.update_progress(100)
                    self.config.status_label.config(text="Processamento concluído!", foreground="green")
                    msg = f"Concluído!\nMP3: {format_file_size(mp3_size)}\nTXT: {format_file_size(txt_size)}"
                    if delete_mp3:
                        msg += "\n(MP3 deletado conforme solicitado)"
                    self.config.show_info(msg)
            finally:
                self.is_processing = False
                if self.config:
                    self.config.enable_button()
                    if not self.is_processing:  # Limpa status se não houver erro pendente
                        self.config.status_label.config(text="", foreground="blue")

        threading.Thread(target=task, daemon=True).start()