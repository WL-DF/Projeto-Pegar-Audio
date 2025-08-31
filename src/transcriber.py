# transcriber.py
import os
import time
import threading
import warnings

# whisper (OpenAI whisper) é pesado e requer torch.
# devemos importar dentro dos métodos para evitar import pesado ao iniciar processo que não usa transcrição.
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

class Transcriber:
    """Transcrição com whisper (local via PyTorch)."""

    def __init__(self, progress_callback=None):
        self.progress_callback = progress_callback
        self.model = None
        self.is_transcribing = False

    def _report(self, value):
        try:
            if self.progress_callback:
                self.progress_callback(int(value))
        except Exception:
            pass

    def load_model(self, model_name="base"):
        """Carrega o modelo Whisper (lazy)."""
        if self.model is None:
            try:
                import whisper
                import torch
                device = "cuda" if torch.cuda.is_available() else "cpu"
                # Alguns ambientes reclamam de fp16 em CPU — whisper lida com isso internamente
                self.model = whisper.load_model(model_name, device=device)
            except Exception as e:
                raise RuntimeError(f"Falha ao carregar modelo whisper: {e}")
        return self.model

    def _check_audio_non_empty(self, path):
        try:
            size = os.path.getsize(path)
            return size > 1024  # >1KB
        except Exception:
            return False

    def _seconds_to_srt_time(self, seconds):
        """Converte segundos para formato HH:MM:SS,mmm para SRT."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        millis = int((seconds - int(seconds)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"

    def transcribe_audio(self, audio_path, output_srt, model_name="base", language=None):
        """
        Transcreve usando whisper local e gera SRT com timestamps.
        Retorna (True, "") ou (False, "mensagem de erro").
        Tentativas de fallback são feitas se resultado vier vazio.
        """
        try:
            if not os.path.exists(audio_path):
                return False, f"Arquivo de áudio não encontrado: {audio_path}"
            if not self._check_audio_non_empty(audio_path):
                return False, "Arquivo de áudio vazio ou inválido."

            model = self.load_model(model_name)
            self.is_transcribing = True

            # iniciar thread que simula progresso
            def simulate_progress():
                p = 40
                while self.is_transcribing and p < 95:
                    time.sleep(0.8)
                    p += 3
                    self._report(p)
            t = threading.Thread(target=simulate_progress, daemon=True)
            t.start()

            # 1ª tentativa: transcrição padrão
            options = {}
            if language:
                options['language'] = language
            result = model.transcribe(audio_path, **options)

            segments = result.get("segments", []) if isinstance(result, dict) else getattr(result, "segments", [])

            # se segments vazio, tenta nova passagem com diferentes opções (fallback)
            if not segments:
                # tentativa 2: forçar idioma PT e aumentar beam (se suportado)
                try:
                    fallback_opts = {'language': language or 'pt', 'task': 'transcribe'}
                    result2 = model.transcribe(audio_path, **fallback_opts)
                    segments2 = result2.get("segments", []) if isinstance(result2, dict) else getattr(result2, "segments", [])
                    if segments2:
                        segments = segments2
                except Exception:
                    # não fatal — continuamos
                    pass

            self.is_transcribing = False
            self._report(100)

            if not segments:
                # grava log de debug para inspeção
                try:
                    dbg_path = os.path.splitext(audio_path)[0] + ".transcribe_debug.txt"
                    with open(dbg_path, "w", encoding="utf-8") as f:
                        f.write("Transcrição vazia — verifique o arquivo de áudio e o modelo.\n")
                    return False, "Transcrição vazia (resultado em debug)."
                except Exception:
                    return False, "Transcrição vazia."

            # gera SRT
            with open(output_srt, "w", encoding="utf-8") as f:
                for i, segment in enumerate(segments, start=1):
                    start_time = self._seconds_to_srt_time(segment.get("start", 0.0))
                    end_time = self._seconds_to_srt_time(segment.get("end", 0.0))
                    text = segment.get("text", "").strip()
                    f.write(f"{i}\n{start_time} --> {end_time}\n{text}\n\n")

            return True, ""
        except Exception as e:
            self.is_transcribing = False
            return False, f"Erro na transcrição: {e}"