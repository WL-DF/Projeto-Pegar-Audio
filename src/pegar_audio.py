import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import whisper
import sys

def check_dependencies():
    """Verifica dependências básicas."""
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        print("FFmpeg encontrado.")
    except FileNotFoundError:
        print("Erro: FFmpeg não encontrado. Configure o PATH.")
        sys.exit(1)
    try:
        tk.Tk().destroy()  # Testa Tkinter
        print("Tkinter funcionando.")
    except:
        print("Erro: Tkinter não instalado.")
        sys.exit(1)

def extract_audio(video_path, output_mp3):
    """Extrai áudio de vídeo e salva como MP3."""
    try:
        subprocess.run(['ffmpeg', '-i', video_path, '-vn', '-ar', '44100',
                       '-ac', '2', '-b:a', '192k', output_mp3], check=True,
                       capture_output=True, text=True)
        return True
    except subprocess.CalledProcessError as e:
        return str(e.stderr)
    except Exception as e:
        return str(e)

def transcribe_audio(audio_path, output_txt):
    """Transcreve áudio para texto usando Whisper."""
    try:
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        with open(output_txt, 'w', encoding='utf-8') as f:
            f.write(result["text"])
        return True
    except Exception as e:
        return str(e)

def process_video():
    """Função principal de processamento em thread."""
    video_path = entry_video.get()
    if not video_path or not os.path.exists(video_path):
        messagebox.showerror("Erro", "Selecione vídeo válido.")
        return
    base_name = os.path.splitext(os.path.basename(video_path))[0]
    output_dir = os.path.dirname(video_path)
    output_mp3 = os.path.join(output_dir, f"{base_name}.mp3")
    output_txt = os.path.join(output_dir, f"{base_name}.txt")
    progress['value'] = 0
    status_label.config(text="Extraindo áudio...")
    audio_result = extract_audio(video_path, output_mp3)
    if audio_result is not True:
        messagebox.showerror("Erro", f"Erro: {audio_result}")
        status_label.config(text="")
        return
    progress['value'] = 50
    if var_transcribe.get():
        status_label.config(text="Transcrevendo áudio...")
        transcribe_result = transcribe_audio(output_mp3, output_txt)
        if transcribe_result is not True:
            messagebox.showerror("Erro", f"Erro: {transcribe_result}")
            status_label.config(text="")
            return
    progress['value'] = 100
    status_label.config(text="")
    messagebox.showinfo("Sucesso", "Processo concluído!")

def start_processing():
    """Inicia processamento em thread separada."""
    threading.Thread(target=process_video, daemon=True).start()

def select_video():
    """Seleciona arquivo de vídeo."""
    file_path = filedialog.askopenfilename(
        filetypes=[("Vídeos", "*.mp4 *.avi *.mkv")]
    )
    if file_path:
        entry_video.delete(0, tk.END)
        entry_video.insert(0, file_path)

# Inicia com verificação
print("Iniciando programa...")
check_dependencies()
try:
    root = tk.Tk()
    root.title("Pegar Áudio")
    root.geometry("400x200")
    tk.Label(root, text="Caminho do Vídeo:").pack(pady=5)
    entry_video = tk.Entry(root, width=50)
    entry_video.pack()
    tk.Button(root, text="Selecionar Vídeo", command=select_video).pack(pady=5)
    var_transcribe = tk.BooleanVar()
    tk.Checkbutton(root, text="Transcr. TXT", variable=var_transcribe).pack(pady=5)
    tk.Button(root, text="Processar", command=start_processing).pack(pady=10)
    progress = ttk.Progressbar(root, length=300, mode='determinate')
    progress.pack(pady=5)
    status_label = tk.Label(root, text="")
    status_label.pack()
    print("Janela iniciada com sucesso!")
    root.mainloop()
except Exception as e:
    print(f"Erro ao iniciar janela: {e}")
    sys.exit(1)