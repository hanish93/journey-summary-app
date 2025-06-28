FROM nvcr.io/nvidia/pytorch:23.08-py3

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libgl1-mesa-glx \
    poppler-utils \
    graphviz \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install specific versions for performance
RUN pip install --no-cache-dir \
    efficientnet_pytorch==0.7.1 \
    pytorch_lightning==2.0.9 \
    torchmetrics==1.0.3 \
    opencv-python-headless==4.8.0.76 \
    fpdf2==2.7.7 \
    wordcloud==1.9.2

# Copy application
COPY . .

# Set environment variables for performance
ENV OMP_NUM_THREADS=1
ENV CUDA_LAUNCH_BLOCKING=0
ENV TORCH_CUDNN_V8_API_ENABLED=1

EXPOSE 5000

# Optimized startup command
CMD ["gunicorn", "app.main:app", "--bind", "0.0.0.0:5000", \
     "--workers", "2", "--threads", "4", "--worker-class", "uvicorn.workers.UvicornWorker"]