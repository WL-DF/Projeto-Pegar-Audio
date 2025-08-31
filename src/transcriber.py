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

    def transcribe_audio(self, audio_path, output_txt, model_name="base", language=None):
        """
        Transcreve usando whisper local.
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

            text = result.get("text", "") if isinstance(result, dict) else getattr(result, "text", "")

            # se texto vazio, tenta nova passagem com diferentes opções (fallback)
            if not text or text.strip() == "":
                # tentativa 2: forçar idioma PT e aumentar beam (se suportado)
                try:
                    fallback_opts = {'language': language or 'pt', 'task': 'transcribe'}
                    result2 = model.transcribe(audio_path, **fallback_opts)
                    text2 = result2.get("text", "") if isinstance(result2, dict) else getattr(result2, "text", "")
                    if text2 and text2.strip():
                        text = text2
                except Exception:
                    # não fatal — continuamos
                    pass

            self.is_transcribing = False
            self._report(100)

            if not text or text.strip() == "":
                # grava log de debug para inspeção
                try:
                    dbg_path = os.path.splitext(audio_path)[0] + ".transcribe_debug.txt"
                    with open(dbg_path, "w", encoding="utf-8") as f:
                        f.write("Transcrição vazia — verifique o arquivo de áudio e o modelo.\n")
                    return False, "Transcrição vazia (resultado em debug)."
                except Exception:
                    return False, "Transcrição vazia."
            # grava texto
            with open(output_txt, "w", encoding="utf-8") as f:
                f.write(text.strip())

            return True, ""
        except Exception as e:
            self.is_transcribing = False
            return False, f"Erro na transcrição: {e}"
