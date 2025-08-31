import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from ttkthemes import ThemedTk
import sys
from utils import format_file_size
import os

def create_gui(processor):
    """Cria e configura a interface gráfica."""
    try:
        root = ThemedTk(theme="arc")
        root.title("Pegar Áudio - Extração e Transcrição")
        root.geometry("500x350")  # Aumentado para acomodar informações adicionais
        root.configure(bg="#f0f0f0")
        root.resizable(False, False)

        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill="both", expand=True)

        title_label = ttk.Label(main_frame, text="Pegar Áudio", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=(0, 15))

        video_frame = ttk.Frame(main_frame)
        video_frame.pack(fill="x", pady=5)
        ttk.Label(video_frame, text="Caminho do Vídeo:").pack(side="left", padx=5)
        entry_video = ttk.Entry(video_frame, width=40)
        entry_video.pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(video_frame, text="Selecionar", command=lambda: select_video(entry_video, file_info_label)).pack(side="left")

        # Label para informações do arquivo
        file_info_label = ttk.Label(main_frame, text="", font=("Helvetica", 9), foreground="gray")
        file_info_label.pack(pady=2)

        var_transcribe = tk.BooleanVar(value=True)
        transcribe_check = ttk.Checkbutton(main_frame, text="Transcrição para TXT", variable=var_transcribe)
        transcribe_check.pack(pady=5)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        process_button = ttk.Button(
            button_frame, 
            text="Processar", 
            command=lambda: on_process_click(processor, entry_video.get(), var_transcribe.get(), process_button, status_label),
            width=15
        )
        process_button.pack()

        # Frame para a barra de progresso
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill="x", pady=10)
        
        progress = ttk.Progressbar(progress_frame, length=400, mode="determinate")
        progress.pack(side="left", fill="x", expand=True)
        
        # Label de porcentagem
        progress_label = ttk.Label(progress_frame, text="0%", width=4)
        progress_label.pack(side="right", padx=(5, 0))

        status_label = ttk.Label(main_frame, text="", font=("Helvetica", 10), foreground="blue")
        status_label.pack(pady=5)

        # Configuração com métodos de callback
        config = type('Config', (), {})()
        config.progress = progress
        config.progress_label = progress_label
        config.status_label = status_label
        config.show_error = lambda msg: show_error_message(msg, status_label)
        config.show_info = lambda msg: show_info_message(msg, status_label)
        config.enable_button = lambda: process_button.config(state="normal")
        config.disable_button = lambda: process_button.config(state="disabled")
        config.update_progress = lambda value: update_progress_bar(progress, progress_label, value)

        processor.config = config

        print("Janela iniciada com sucesso!")
        root.mainloop()

    except Exception as e:
        print(f"Erro ao criar GUI: {e}")
        sys.exit(1)

def select_video(entry, info_label):
    """Seleciona arquivo de vídeo e atualiza o campo."""
    file_path = filedialog.askopenfilename(
        title="Selecionar Vídeo",
        filetypes=[("Vídeos", "*.mp4 *.avi *.mkv"), ("Todos os arquivos", "*.*")]
    )
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)
        
        # Atualiza informações do arquivo
        try:
            file_size = os.path.getsize(file_path)
            info_label.config(text=f"Arquivo selecionado: {os.path.basename(file_path)} ({format_file_size(file_size)})")
        except:
            info_label.config(text=f"Arquivo selecionado: {os.path.basename(file_path)}")

def on_process_click(processor, video_path, transcribe, button, status_label):
    """Callback para o botão de processar."""
    button.config(state="disabled")
    status_label.config(text="Validando...", foreground="blue")
    
    # Pequeno delay para permitir a atualização da interface
    button.after(100, lambda: processor.process_video(video_path, transcribe))

def show_error_message(msg, status_label):
    """Mostra mensagem de erro na interface."""
    status_label.config(text=f"Erro: {msg}", foreground="red")
    messagebox.showerror("Erro", msg)

def show_info_message(msg, status_label):
    """Mostra mensagem de informação na interface."""
    status_label.config(text=msg, foreground="green")
    messagebox.showinfo("Sucesso", msg)

def update_progress_bar(progress_bar, progress_label, value):
    """Atualiza a barra de progresso."""
    progress_bar['value'] = value
    progress_label.config(text=f"{value}%")