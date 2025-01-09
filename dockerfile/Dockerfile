FROM ubuntu:22.04

# Set non-interactive mode to avoid prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies for curl and sudo
RUN apt-get update && apt-get install -y \
    curl \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Download ollama CLI
RUN curl -fsSL https://ollama.com/install.sh | sh

# Download python
RUN apt-get update && apt-get install -y python3 python3-pip curl sudo

# Download requirements 
RUN pip install ollama
RUN pip install llama-index
RUN pip install chromadb

# Set the working directory for your project
WORKDIR /home

