import os
from huggingface_hub import hf_hub_download
import subprocess

# Settings
model_repo = "TheBloke/CodeLlama-7B-GGUF"  # Any GGUF model repo
model_file = "codellama-7b.Q5_K_M.gguf"    # Choose a model file (.gguf or .ggml)
quantize_to = "Q4_K_M"                     # Target quantization type
output_model = "codellama-7b.Q4_K_M.gguf"  # Output file name

# Paths
output_dir = "./models"
os.makedirs(output_dir, exist_ok=True)

print("[1] Downloading model from Hugging Face...")
local_model_path = hf_hub_download(
    repo_id=model_repo,
    filename=model_file,
    local_dir=output_dir,
    local_dir_use_symlinks=False
)

print(f"[2] Model downloaded: {local_model_path}")

# Check for llama.cpp quantize tool
quantize_exe = "./llama.cpp/quantize"
if not os.path.exists(quantize_exe):
    raise FileNotFoundError("quantize tool not found. Build llama.cpp first.")

output_path = os.path.join(output_dir, output_model)

print(f"[3] Quantizing model to {quantize_to}...")
quant_cmd = [quantize_exe, local_model_path, output_path, quantize_to]

subprocess.run(quant_cmd, check=True)

print(f"[✅] Quantization complete: {output_path}")


modelfile_path = os.path.join(output_dir, "Modelfile")
with open(modelfile_path, "w") as f:
    f.write(f"FROM ./{output_model}\n")
    f.write("PARAMETER temperature 0.2\n")

print(f"[📦] Modelfile created at {modelfile_path}")