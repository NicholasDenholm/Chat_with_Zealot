import torch
print(torch.__version__)
print(torch.version.cuda)
print(torch.cuda.is_available())  # Should return True if CUDA is available
print(torch.cuda.get_device_name(0))  # Should show the name of the GPU

# Attempts
# Do this: pip install torch==1.12.0+cu118 torchvision==0.13.0+cu117 torchaudio==0.12.0 -f https://download.pytorch.org/whl/torch_stable.html
# ran this instead: pip install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1
# Did this: pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
# Try this: python -c "import torch; print(torch.rand(2,3).cuda())"

# Switching between versions:
'''
11.7
export PATH=/usr/local/cuda-11.7/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-11.7/lib64:$LD_LIBRARY_PATH
export CUDA_HOME=/usr/local/cuda-11.7

12.8
export PATH=/usr/local/cuda-12.8/bin:$PATH
export LD_LIBRARY_PATH=/usr/local/cuda-12.8/lib64:$LD_LIBRARY_PATH
export CUDA_HOME=/usr/local/cuda-12.8

'''
