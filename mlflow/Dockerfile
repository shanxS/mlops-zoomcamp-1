FROM mcr.microsoft.com/devcontainers/python:1-3.12-bullseye

WORKDIR /app

VOLUME /mlflow/mlruns
VOLUME /mlflow/mlartifacts

EXPOSE 5000

ENV MLFLOW_TRACKING_URI=http://127.0.0.1:5000
ENV MLFLOW_ARTIFACT_URI=file:///mlflow/mlartifacts
ENV MLFLOW_BACKEND_STORE_URI=file:///mlflow/mlruns

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install mlflow==2.20.4

CMD mlflow server --host 0.0.0.0 --port 5000 --backend-store-uri ${MLFLOW_BACKEND_STORE_URI} --default-artifact-root ${MLFLOW_ARTIFACT_URI} --dev