#!/bin/bash

docker build -t mlflow-dev .
docker rm -f mlflow-server