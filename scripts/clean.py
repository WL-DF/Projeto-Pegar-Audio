import os
import glob
import shutil

def clean_project():
    """Limpa arquivos temporários e de cache do projeto."""
    
    print("🧹 Limpando projeto...")
    
    items_to_remove = [
        "build/",
        "dist/",
        "__pycache__/",
        "src/__pycache__/",
        "*.pyc",
        "*.log",
        "*.spec",
        "*.mp3",
        "*.txt",
        "Pegar_Audio.spec"
    ]
    
    removed_count = 0
    
    for item in items_to_remove:
        if item.endswith('/'):
            folder = item[:-1]
            if os.path.exists(folder):
                shutil.rmtree(folder, ignore_errors=True)
                print(f"📁 Removendo pasta: {folder}")
                removed_count += 1
        else:
            for file_path in glob.glob(item, recursive=True):
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"📄 Removendo arquivo: {file_path}")
                    removed_count += 1
    
    # Remove diretórios __pycache__ recursivamente
    for root, dirs, files in os.walk('.', topdown=False):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                dir_path = os.path.join(root, dir_name)
                shutil.rmtree(dir_path, ignore_errors=True)
                print(f"🗑️ Removendo: {dir_path}")
                removed_count += 1
    
    print(f"✅ Limpeza concluída! {removed_count} itens removidos.")

if __name__ == "__main__":
    clean_project()