FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

RUN useradd -ms /bin/bash vscode
USER vscode