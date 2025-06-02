from typing import List
from prefect import flow, get_run_logger, task
from prefect.context import get_run_context
from prefect.cache_policies import INPUTS
from prefect.docker import DockerImage
import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import Pipeline
import mlflow
from mlflow.models import infer_signature
import click

@task
def data_loader(url: str = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-03.parquet'):
    mlflow.log_param("data_url", url)
    df = pd.read_parquet(url)
    get_run_logger().info(f"[Q3] num rows:{df.shape[0]} ")
    mlflow.log_metric("input_length", df.shape[0])
    return df

@task
def transform_data(df: pd.DataFrame):
    
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df.duration = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)]
    
    categorical = ['PULocationID', 'DOLocationID']
    df[categorical] = df[categorical].astype(str)
    X = df[categorical].to_dict(orient='records')

    get_run_logger().info(f"[Q4] num rows:{len(X)} ")

    return X, df['duration']

def training_pipeline():
    return Pipeline(
        steps=[
            ("dict_vectorizer", DictVectorizer()),
            ("linear_regression", LinearRegression())
        ]
    )

@task
def train_model(X, y):
    
    signature = infer_signature(X, y)
    pipeline = training_pipeline()
    
    pipeline.fit(X, y)
    get_run_logger().info(f"[Q5] intercept of trained model:{pipeline.named_steps["linear_regression"].intercept_} ")
    mlflow.log_metric("intercept", pipeline.named_steps["linear_regression"].intercept_)

    mlflow.sklearn.log_model(
        pipeline, 
        artifact_path="pipeline",
        signature=signature
    )

@flow
def HW3():
    mlflow.set_experiment("HW3")
    with mlflow.start_run(run_name=get_run_context().flow_run.name): # type: ignore
        df = data_loader()
        X,y = transform_data(df)
        train_model(X,y)

@click.command()
@click.option("--remote-deploy", is_flag=True, help="Deploy to remote")
def start(remote_deploy: bool):
    if remote_deploy:
        flow_name = "hw-3"
        HW3.deploy(
            name=flow_name,
            work_pool_name="docker-pool",
            image=DockerImage(
                name=f"nexus4shashank/mlopszoomcamp:{flow_name}",
                dockerfile="03-orchestration/prefect_base_dockerfile",
                context="../"
            )
        )
    else:
        HW3()

if __name__ == "__main__":
    start()