FROM runpod/pytorch:2.2.0-py3.10-cuda12.1.1-devel-ubuntu22.04

# Install audio + compiler tools
RUN apt-get update && apt-get install -y ffmpeg libsndfile1 build-essential && rm -rf /var/lib/apt/lists/*

# Copy & install Python dependencies
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy your handler
COPY rp_handler.py /workspace/

# Force download of model during build (saves cold-start time)
RUN python -c "import nemo.collections.asr as n; n.models.ASRModel.from_pretrained(model_name='nvidia/parakeet-tdt-0.6b-v2')"

# Start server
CMD ["python", "/workspace/rp_handler.py"]
