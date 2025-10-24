FROM python:3.11-slim
WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc && rm -rf /var/lib/apt/lists/*

COPY requirements-defender.txt ./
RUN pip install --no-cache-dir -r requirements-defender.txt

COPY defender_ai.py ./

CMD ["python", "defender_ai.py"]
