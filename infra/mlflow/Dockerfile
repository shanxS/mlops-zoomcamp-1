FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

WORKDIR /app

EXPOSE 5000

ENV MLFLOW_TRACKING_URI=http://127.0.0.1:5000
RUN apt-get update
RUN pip install --upgrade pip
RUN pip install mlflow==2.20.4

CMD mlflow server --host 0.0.0.0 --port 5000 --backend-store-uri file:///mlflow/mlruns --artifacts-destination file:///mlflow/mlartifacts  --dev