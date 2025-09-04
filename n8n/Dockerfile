FROM n8nio/n8n:1.52.0-debian

USER root

RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

USER node
