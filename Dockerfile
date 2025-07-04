FROM nvcr.io/nvidia/pytorch:23.08-py3

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libgl1-mesa-glx \
    libglib2.0-0 \
    poppler-utils \
    graphviz \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install specific versions for compatibility
RUN pip install --no-cache-dir \
    opencv-python-headless==4.7.0.72 \
    celery==5.3.4 \
    eventlet==0.33.3 \
    redis \
    torch==2.0.1 \
    torchvision==0.15.2 \
    efficientnet_pytorch==0.7.1 \
    pytorch_lightning==2.0.9 \
    transformers==4.31.0 \
    fpdf2==2.7.7 \
    wordcloud==1.9.2 \
    matplotlib==3.7.2 \
    pandas==2.0.3 \
    scikit-learn==1.3.0

# Copy application
COPY . /app
WORKDIR /app

# Set environment variables for performance
ENV OMP_NUM_THREADS=1
ENV CUDA_LAUNCH_BLOCKING=0
ENV TORCH_CUDNN_V8_API_ENABLED=1

EXPOSE 5000