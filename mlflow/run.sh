#!/bin/bash

docker stop mlflow-server

while docker ps | grep mlflow-server; do
  echo "Waiting for mlflow-server to stop..."
  sleep 1
done

docker rm mlflow-server 2>/dev/null || true

docker run -d --name mlflow-server -p 5001:5000 \
  -v /tmp/mlruns:/mlflow/mlruns \
  -v /tmp/mlartifacts:/mlflow/mlartifacts \
  mlflow-dev

export MLFLOW_TRACKING_URI=http://host.docker.internal:5001
echo "MLflow server started. Set MLFLOW_TRACKING_URI to http://host.docker.internal:5001 in your devcontainer"  