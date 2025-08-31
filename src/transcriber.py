import whisper
import warnings
import time
import threading
import os
# Suprime avisos específicos do Whisper
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

class Transcriber:
    """Classe para transcrição de áudio com Whisper."""
    
    def __init__(self, progress_callback=None):
        self.progress_callback = progress_callback
        self.model = None
        self.is_transcribing = False
        
    def load_model(self):
        """Carrega o modelo Whisper."""
        if self.model is None:
            self.model = whisper.load_model("base")
        return self.model
    
    def transcribe_audio(self, audio_path, output_txt):
        """Transcreve áudio para texto usando Whisper."""
        try:
            if not os.path.exists(audio_path):
                return False, f"Arquivo de áudio não encontrado: {audio_path}"
                
            model = self.load_model()
            self.is_transcribing = True
            
            # Inicia uma thread para simular o progresso durante a transcrição
            def simulate_progress():
                progress = 50
                while self.is_transcribing and progress < 100:
                    time.sleep(0.5)
                    progress += 1
                    if self.progress_callback:
                        self.progress_callback(progress)
            
            progress_thread = threading.Thread(target=simulate_progress)
            progress_thread.daemon = True
            progress_thread.start()
            
            # Transcreve sem o parâmetro progress_callback que não é suportado
            result = model.transcribe(audio_path, verbose=False)
            
            # Para a simulação de progresso
            self.is_transcribing = False
            
            with open(output_txt, 'w', encoding='utf-8') as f:
                f.write(result["text"])
                
            return True, ""
            
        except Exception as e:
            self.is_transcribing = False
            return False, f"Erro na transcrição: {str(e)}"