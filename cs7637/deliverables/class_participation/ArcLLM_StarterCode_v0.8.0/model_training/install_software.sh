# Create & activate virtual environment
python -m venv lora_env
# use one line or the other to activate the environment
source lora_env/bin/activate           # Linux/Mac ~ comment out line if running in Windows
#lora_env\Scripts\activate             # Windows ~ uncomment line for Windows OS

# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install PyTorch (choose ONE)
# GPU (CUDA 12.1 – recommended for RTX 30/40/50 series)
# pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121   # <-- uncoment line for GPU

# CPU-only (slower, but works everywhere)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu     # <-- uncoment line for CPU-only

# Install core libraries
pip install transformers==5.3.0 \
    huggingface-hub==1.7.2 \
    peft==0.18.1 \
    accelerate==1.13.0 \
    sentencepiece==0.2.1 \
