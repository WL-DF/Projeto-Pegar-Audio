import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from ttkthemes import ThemedTk
import sys
import os
from utils import format_file_size

def create_gui(processor):
    try:
        root = ThemedTk(theme="arc")
        root.title("Pegar Áudio - Extração e Transcrição")
        root.geometry("540x380")
        root.configure(bg="#f0f0f0")
        root.resizable(False, False)

        main_frame = ttk.Frame(root, padding="16")
        main_frame.pack(fill="both", expand=True)

        title_label = ttk.Label(main_frame, text="Pegar Áudio", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=(0, 12))

        video_frame = ttk.Frame(main_frame)
        video_frame.pack(fill="x", pady=6)
        ttk.Label(video_frame, text="Caminho do Vídeo:").pack(side="left", padx=5)
        entry_video = ttk.Entry(video_frame, width=46)
        entry_video.pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(video_frame, text="Selecionar", command=lambda: select_video(entry_video, file_info_label)).pack(side="left")

        file_info_label = ttk.Label(main_frame, text="", font=("Helvetica", 9), foreground="gray")
        file_info_label.pack(pady=2)

        var_transcribe = tk.BooleanVar(value=True)
        transcribe_check = ttk.Checkbutton(main_frame, text="Transcrição para TXT", variable=var_transcribe)
        transcribe_check.pack(pady=6)

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        process_button = ttk.Button(button_frame, text="Processar", width=16,
                                    command=lambda: on_process_click(processor, entry_video.get(), var_transcribe.get(), process_button, status_label))
        process_button.pack()

        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill="x", pady=10)
        progress = ttk.Progressbar(progress_frame, length=420, mode="determinate")
        progress.pack(side="left", fill="x", expand=True)
        progress_label = ttk.Label(progress_frame, text="0%", width=5)
        progress_label.pack(side="right", padx=(6,0))

        status_label = ttk.Label(main_frame, text="", font=("Helvetica", 10), foreground="blue")
        status_label.pack(pady=6)

        # Config object for callbacks
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

        root.mainloop()
    except Exception as e:
        print(f"Erro ao criar GUI: {e}")
        sys.exit(1)

def select_video(entry, info_label):
    file_path = filedialog.askopenfilename(title="Selecionar Vídeo", filetypes=[("Vídeos", "*.mp4 *.avi *.mkv *.mov *.flv"), ("Todos", "*.*")])
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)
        try:
            size = os.path.getsize(file_path)
            info_label.config(text=f"{os.path.basename(file_path)} ({format_file_size(size)})")
        except:
            info_label.config(text=f"{os.path.basename(file_path)}")

def on_process_click(processor, video_path, transcribe, button, status_label):
    button.config(state="disabled")
    status_label.config(text="Preparando...", foreground="blue")
    # slight delay to let UI update
    button.after(120, lambda: processor.process_video(video_path, transcribe))

def show_error_message(msg, status_label):
    status_label.config(text=f"Erro: {msg}", foreground="red")
    messagebox.showerror("Erro", msg)

def show_info_message(msg, status_label):
    status_label.config(text=msg, foreground="green")
    messagebox.showinfo("Sucesso", msg)

def update_progress_bar(progress_bar, progress_label, value):
    try:
        v = int(value)
    except:
        v = 0
    if v < 0: v = 0
    if v > 100: v = 100
    progress_bar['value'] = v
    progress_label.config(text=f"{v}%")
