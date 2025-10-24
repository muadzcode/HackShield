FROM python:3.11-slim
WORKDIR /app

# Install minimal runtime deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc && rm -rf /var/lib/apt/lists/*

COPY requirements-attacker.txt ./
RUN pip install --no-cache-dir -r requirements-attacker.txt

COPY attacker_ai.py ./

CMD ["python", "attacker_ai.py"]
