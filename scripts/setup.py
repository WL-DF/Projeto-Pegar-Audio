import subprocess
import sys
import os

def run_command(cmd):
    """Executa um comando e mostra output em tempo real."""
    print(f"Executando: {cmd}")
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
    
    for line in process.stdout:
        print(line, end='')
    
    process.wait()
    return process.returncode

def main():
    print("🚀 Configurando o projeto Pegar Áudio...")
    
    # Verifica se o UV está instalado
    try:
        subprocess.run(["uv", "--version"], check=True, capture_output=True)
        print("✅ UV encontrado.")
    except:
        print("📦 Instalando UV...")
        run_command("pip install uv")
    
    # Verifica se o Python 3.12 está disponível
    try:
        subprocess.run(["uv", "python", "list"], check=True, capture_output=True)
    except:
        print("🐍 Instalando Python 3.12...")
        run_command("uv python install 3.12")
    
    # Cria ambiente virtual com Python 3.12
    if not os.path.exists("pegaraudio-env-312"):
        print("🔧 Criando ambiente virtual...")
        run_command("uv venv --python 3.12 pegaraudio-env-312")
    
    # Compila requirements.txt
    print("📋 Compilando dependências...")
    run_command("uv pip compile requirements.in -o requirements.txt")
    
    # Instala dependências
    print("📦 Instalando dependências...")
    run_command("uv pip install -r requirements.txt")
    
    print("✅ Configuração concluída!")
    print("\n📝 Próximos passos:")
    print("1. Ative o ambiente virtual:")
    print("   PowerShell: .\\pegaraudio-env-312\\Scripts\\Activate.ps1")
    print("   CMD: .\\pegaraudio-env-312\\Scripts\\activate.bat")
    print("2. Execute o projeto: python src\\main.py")
    print("3. Para build: python scripts\\build.py")

if __name__ == "__main__":
    main()