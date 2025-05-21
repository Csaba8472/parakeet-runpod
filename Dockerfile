FROM runpod/pytorch:2.1.2-cuda12.1.0-ubuntu20.04
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt
COPY rp_handler.py /workspace/
CMD ["python", "/workspace/rp_handler.py"]
