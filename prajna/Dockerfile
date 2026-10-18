FROM python:3.11-slim

WORKDIR /workspace

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY prajna/requirements.txt /workspace/requirements.txt
RUN pip install --no-cache-dir -r /workspace/requirements.txt

COPY prajna /workspace/prajna

ENV PYTHONPATH=/workspace

EXPOSE 8080

CMD ["uvicorn", "prajna.app.main:app", "--host", "0.0.0.0", "--port", "8080"]
