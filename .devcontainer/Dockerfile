FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye as base

# Set working directory
WORKDIR /workspaces

RUN apt-get update
RUN apt-get install -y docker.io 
RUN pip install --upgrade pip

# Install uv
RUN pipx install uv
ENV UV_HTTP_TIMEOUT=300 
ENV UV_LINK_MODE=copy
