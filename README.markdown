# 🎵 Pegar Áudio

Extrai áudio de vídeos e transcreve para texto usando IA (OpenAI Whisper).

## ✨ Funcionalidades

- Extrai áudio de vídeos (MP4, AVI, MKV, MOV, WMV, FLV) usando FFmpeg embutido.
- Transcreve áudio para texto em formato SRT usando Whisper AI.
- Interface gráfica moderna e intuitiva com Tkinter e temas personalizados.
- Barra de progresso animada para acompanhar o processamento. ⏳
- Opção para excluir o arquivo MP3 após transcrição. 🗑️
- Suporte a modelos Whisper localmente (base, small, etc.).
- Build único para distribuição (via PyInstaller). 📦

## 🚀 Como Usar

### Pré-requisitos

- **Sistema Operacional**: Windows 10 ou superior. 💻
- **Python**: Versão 3.12 recomendada (gerenciada via UV). 🐍
- **Dependências**: Automatizadas pelo script `setup.py`. 🔧

### 🔧 Instalação

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/WL-DF/Projeto-Pegar-Audio
   cd pegaraudio-projeto
   ```

2. **Configure o ambiente**:
   - Execute o script de configuração:🛠️
     ```bash
     python scripts/setup.py
     ```
   - Crie um ambiente virtual (se necessário):🌐
     ```bash
     uv venv --python 3.12 pegaraudio-env-312
     ```
   - Ative o ambiente e instale dependências:📥
     ```bash
     uv run python src/main.py
     ```

3. ▶️ **Executar a aplicação**:
   - Após a configuração, inicie a GUI:
     ```bash
     uv run python src/main.py
     ```

### 🎮 Uso

- **Selecionar Vídeo**: Clique em "Selecionar" para escolher um arquivo de vídeo suportado. 📹
- **Transcrição**: Ative a opção "Transcrição para SRT" para gerar legendas. 🎤
- **Excluir MP3**: Marque "Excluir o arquivo MP3 após transcrição?" se desejar. 🗑️
- **Processar**: Clique em "Processar" para iniciar a extração e/ou transcrição. ✅

### 📦 Build Executável

Para criar um executável standalone:
1. Execute o script de build: 🛠️
   ```bash
   python scripts/build.py
   ```
   - Use `python scripts/build.py --light` para uma versão leve (sem Whisper/Torch).
2. O executável estará em `dist/Pegar_Audio.exe`.

### 🧹 Limpeza

Para remover arquivos temporários:
```bash
python scripts/clean.py
```

## 📋 Estrutura do Projeto

```
PEGARAUDIO-PROJETO/
├── docs/
│   └── .vscode/
├── ffmpeg/
│   └── bin/
│       └── ffmpeg.exe
├── pegaraudio-env-312/
├── scripts/
│   ├── build.py
│   ├── clean.py
│   └── setup.py
├── src/
│   ├── __pycache__/
│   ├── audio_extractor.py
│   ├── audio_processor.py
│   ├── config.py
│   ├── gui.py
│   ├── main.py
│   ├── pegar_audio.py
│   ├── progress_manager.py
│   ├── transcriber.py
│   ├── utils.py
│   └── validations.py
├── .gitignore
├── 4.66.1
├── LICENSE
├── pyinstaller_config.py
├── requirements.in
├── requirements.txt
├── README.md (Atualizado em 31/08/2025 às 11:15 AM -03)
```

## 🛠 Dependências

Listadas em `requirements.txt`, geradas a partir de `requirements.in`. Principais:
- `openai-whisper==20250625`
- `pyinstaller>=6.8.0`
- `pillow>=11.3.0`
- `ttkthemes>=3.2.2`
- `torch==2.3.1`
- `torchaudio==2.3.1`
- `numpy<2`
- `requests>=2.31.0`
- `tqdm>=4.66.1`

## 📜 Licença

Este projeto está sob a licença [MIT](LICENSE).

## 🤝 Contribuições

Contribuições são bem-vindas! Abra uma issue ou envie um pull request.