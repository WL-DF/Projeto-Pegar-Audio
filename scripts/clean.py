import os
import shutil
import glob

def clean():
    targets = ["build", "dist", "__pycache__", "*.spec", "*.log", "*.pyc"]
    print("Limpando projeto...")
    for t in targets:
        if os.path.isdir(t):
            shutil.rmtree(t, ignore_errors=True)
            print("Removido:", t)
        else:
            for f in glob.glob(t, recursive=True):
                try:
                    os.remove(f)
                    print("Removido arquivo:", f)
                except:
                    pass
    print("Limpeza concluída.")

if __name__ == "__main__":
    clean()
