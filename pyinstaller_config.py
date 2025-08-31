# pyinstaller_config.py
# Configurações para otimizar o build com PyTorch

# Lista de módulos a serem incluídos
hiddenimports = [
    'whisper',
    'ttkthemes',
    'PIL',
    'torch',
    'torchaudio',
    'numpy',
    'numpy.core._multiarray_umath',
    'numpy.core._multiarray_tests',
    'numpy.linalg._umath_linalg',
    'numpy.fft._pocketfft_internal',
    'numpy.random._common',
    'numpy.random._bounded_integers',
    'numpy.random._mt19937',
    'numpy.random._pcg64',
    'numpy.random._philox',
    'numpy.random._sfc64',
    'numpy.random.bit_generator',
    'numpy.random.mtrand',
]

# Excluir módulos desnecessários para reduzir tamanho
excludes = [
    'tkinter',
    'matplotlib',
    'scipy',
    'pandas',
    'sklearn',
    'IPython',
    'jupyter',
    'notebook',
    'qtpy',
    'PyQt5',
    'PySide2',
    'test',
    'unittest',
    'pydoc',
]

# Binários adicionais
binaries = []

# Dados adicionais
datas = []