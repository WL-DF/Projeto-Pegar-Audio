import subprocess
import sys
import os

def run(cmd):
    print(f"$ {cmd}")
    return subprocess.call(cmd, shell=True)

def main():
    print("Configurando o projeto com UV...")
    # compila requirements e instala (via uv)
    run("uv pip compile requirements.in -o requirements.txt")
    run("uv pip install -r requirements.txt")
    print("Concluído. Ative seu ambiente criado pelo UV antes de rodar a aplicação.")
    print("Ex.: uv venv --python 3.12 pegaraudio-env-312  # se não existir")
    print("Depois: uv run python src/main.py")

if __name__ == "__main__":
    main()
