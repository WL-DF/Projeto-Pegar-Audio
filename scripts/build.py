import subprocess
import sys
import os
import shutil

def run(cmd):
    print(f"$ {cmd}")
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    for line in proc.stdout:
        print(line, end="")
    proc.wait()
    return proc.returncode

def main():
    light_mode = "--light" in sys.argv
    print("Iniciando build (modo leve)" if light_mode else "Iniciando build (modo completo com whisper/torch)")

    # atualiza e instala dependências no ambiente ativo
    run("uv pip compile requirements.in -o requirements.txt")
    run("uv pip install -r requirements.txt")

    # limpa
    for d in ["build", "dist"]:
        if os.path.exists(d):
            shutil.rmtree(d, ignore_errors=True)

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

    hidden = ["ttkthemes", "PIL", "numpy", "requests"]
    for h in hidden:
        cmd.append(f"--hidden-import={h}")

    if light_mode:
        # light: não inclui whisper/torch
        cmd.append("--exclude-module=whisper")
        cmd.append("--exclude-module=torch")
        cmd.append("--exclude-module=torchaudio")

    # executa
    return_code = run(" ".join(cmd))
    if return_code == 0:
        print("Build finalizado. Executável em dist/Pegar_Audio.exe")
    else:
        print("Build falhou. Veja logs acima.")
    return return_code

if __name__ == "__main__":
    sys.exit(main())
