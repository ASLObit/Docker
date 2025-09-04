FROM n8nio/n8n:latest

# Instalar ffmpeg
USER root
RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

# Volvemos al usuario normal de n8n
USER node
