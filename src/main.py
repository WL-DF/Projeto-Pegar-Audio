import sys
from gui import create_gui
from audio_processor import AudioProcessor
from config import Config

def main():
    """Ponto de entrada da aplicação."""
    try:
        config = Config()
        processor = AudioProcessor(config)
        create_gui(processor)
    except Exception as e:
        print(f"Erro ao iniciar aplicação: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()