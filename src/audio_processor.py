import os
import threading
from audio_extractor import AudioExtractor
from transcriber import Transcriber
from validations import validate_video_path, validate_output_dir
from progress_manager import ProgressManager
from utils import get_output_paths

class AudioProcessor:
    """Classe para processar áudio e transcrição com validações otimizadas."""
    
    def __init__(self, config):
        self.config = config
        self.is_processing = False
        self.progress_manager = ProgressManager(self.update_progress)
        
        # Inicializa extractor e transcriber com callbacks de progresso
        self.extractor = AudioExtractor(self.handle_extraction_progress)
        self.transcriber = Transcriber(self.handle_transcription_progress)
    
    def handle_extraction_progress(self, progress):
        """Callback para progresso da extração."""
        self.progress_manager.set_progress(progress)
    
    def handle_transcription_progress(self, progress):
        """Callback para progresso da transcrição."""
        self.progress_manager.set_progress(progress)
    
    def update_progress(self, value):
        """Atualiza o progresso na interface."""
        if self.config and hasattr(self.config, 'update_progress'):
            self.config.update_progress(value)
    
    def process_video(self, video_path, transcribe):
        """Processa o vídeo com validações otimizadas."""
        if self.is_processing:
            self.config.show_error("Já existe um processamento em andamento.")
            return
            
        self.is_processing = True
        self.progress_manager.reset()
        self.config.disable_button()
        self.config.update_progress(0)
        self.config.status_label.config(text="Validando...", foreground="blue")
        
        if not video_path:
            self.config.show_error("Selecione um vídeo primeiro.")
            self.is_processing = False
            self.config.enable_button()
            return
            
        # Validações
        is_valid, message = validate_video_path(video_path)
        if not is_valid:
            self.config.show_error(message)
            self.is_processing = False
            self.config.enable_button()
            return
            
        output_dir = os.path.dirname(video_path)
        is_valid, message = validate_output_dir(output_dir)
        if not is_valid:
            self.config.show_error(message)
            self.is_processing = False
            self.config.enable_button()
            return
            
        # Obtém caminhos de saída
        output_mp3, output_txt = get_output_paths(video_path, transcribe)

        def task():
            try:
                self.config.status_label.config(text="Extraindo áudio...", foreground="blue")
                
                # Extrai áudio
                success, message = self.extractor.extract_audio_fast(video_path, output_mp3)
                if not success:
                    self.config.show_error(message)
                    return
                
                # Se não for transcrever, finaliza em 100%
                if not transcribe:
                    self.progress_manager.set_progress(100)
                    self.config.status_label.config(text="Processamento concluído!", foreground="green")
                    
                    # Mostra informações do arquivo gerado
                    if os.path.exists(output_mp3):
                        file_size = os.path.getsize(output_mp3)
                        from utils import format_file_size
                        self.config.show_info(f"Processo concluído! Arquivo: {os.path.basename(output_mp3)} ({format_file_size(file_size)})")
                    else:
                        self.config.show_info("Processo concluído com sucesso!")
                    return
                
                # Transcrição
                self.config.status_label.config(text="Transcrevendo áudio...", foreground="blue")
                success, message = self.transcriber.transcribe_audio(output_mp3, output_txt)
                if not success:
                    self.config.show_error(message)
                    return
                
                # Atualiza a interface para mostrar conclusão
                self.progress_manager.set_progress(100)
                self.config.status_label.config(text="Processamento concluído!", foreground="green")
                
                # Mostra informações dos arquivos gerados
                mp3_size = os.path.getsize(output_mp3) if os.path.exists(output_mp3) else 0
                txt_size = os.path.getsize(output_txt) if os.path.exists(output_txt) else 0
                
                from utils import format_file_size
                message = f"Processo concluído!\nMP3: {format_file_size(mp3_size)}\nTXT: {format_file_size(txt_size)}"
                self.config.show_info(message)
                
            except Exception as e:
                self.config.show_error(f"Erro inesperado: {str(e)}")
            finally:
                self.is_processing = False
                self.config.enable_button()

        # Executa em thread separada
        threading.Thread(target=task, daemon=True).start()