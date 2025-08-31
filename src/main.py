import sys
from config import Config
from audio_processor import AudioProcessor
from gui import create_gui

def main():
    try:
        cfg = Config()
        processor = AudioProcessor(cfg)
        create_gui(processor)
    except Exception as e:
        print(f"Erro ao iniciar aplicação: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
