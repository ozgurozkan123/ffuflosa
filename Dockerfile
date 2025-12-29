FROM ubuntu:24.04

# Install ffuf and Python tooling
RUN apt-get update && apt-get install -y \
    ffuf \
    python3 \
    python3-pip \
    ca-certificates \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

ENV HOST=0.0.0.0
ENV PORT=8000
EXPOSE 8000

CMD ["python3", "server.py"]
