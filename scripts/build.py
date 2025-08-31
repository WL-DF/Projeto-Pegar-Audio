import subprocess
import sys
import os
import shutil

def run_command(cmd):
    print(f"$ {cmd}")
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    for line in process.stdout:
        print(line, end="")
    process.wait()
    return process.returncode

def main():
    print("🔨 Build iniciado com UV + PyInstaller")

    light_mode = "--light" in sys.argv

    # Garante dependências atualizadas
    print("📦 Atualizando dependências…")
    run_command("uv pip compile requirements.in -o requirements.txt")
    run_command("uv pip install -r requirements.txt")

    # Limpa builds anteriores
    for folder in ["build", "dist"]:
        if os.path.exists(folder):
            shutil.rmtree(folder, ignore_errors=True)

    # Comando base do PyInstaller
    cmd = [
        "pyinstaller",
        "src/main.py",
        "--name=Pegar_Audio",
        "--onefile",
        "--windowed",
        "--clean",
        "--noconfirm",
        "--add-data=ffmpeg/bin/ffmpeg.exe;."
    ]

    # Hidden imports (necessários p/ torch/numpy/whisper)
    hidden_imports = ["whisper", "ttkthemes", "PIL", "torch", "torchaudio", "numpy"]
    for imp in hidden_imports:
        cmd.append(f"--hidden-import={imp}")

    # Ícone (se existir)
    if os.path.exists("icon.ico"):
        cmd.append("--icon=icon.ico")

    # Light mode → exclui torch/whisper
    if light_mode:
        print("⚡ Light mode ativo: excluindo whisper/torch do build")
        cmd.append("--exclude-module=torch")
        cmd.append("--exclude-module=torchaudio")
        cmd.append("--exclude-module=whisper")

    return_code = run_command(" ".join(cmd))

    if return_code == 0:
        print("✅ Build concluído com sucesso! Executável em dist/Pegar_Audio.exe")
    else:
        print("❌ Build falhou.")

    return return_code

if __name__ == "__main__":
    sys.exit(main())
