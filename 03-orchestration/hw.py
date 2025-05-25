from prefect import flow, get_run_logger, task
from prefect.cache_policies import INPUTS
from prefect.docker import DockerImage
import pandas as pd
from sklearn.feature_extraction import DictVectorizer

@task(cache_policy=INPUTS)
def data_loader(url: str = 'https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-03.parquet'):
    df = pd.read_parquet(url)
    get_run_logger().info(f"[Q3] num rows:{df.shape[0]} ")
    return df

@task(cache_policy=INPUTS)
def transform_data(df: pd.DataFrame):
    dv = DictVectorizer()
    
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df['duration'] = df.tpep_dropoff_datetime - df.tpep_pickup_datetime
    df.duration = df.duration.dt.total_seconds() / 60
    df = df[(df.duration >= 1) & (df.duration <= 60)]
    
    numerical = ['trip_distance']
    categorical = ['PULocationID', 'DOLocationID']
    
    df[categorical] = df[categorical].astype(str)
    
    dicts = df[categorical + numerical].to_dict(orient='records')
    result = dv.fit_transform(dicts)

    get_run_logger().info(f"[Q4] num rows:{df.shape[0]} ")

    return result

@flow
def HW3():
    df = data_loader()
    transform_data(df)

if __name__ == "__main__":
    flow_name = "hw-3"
    HW3.deploy(
        name=flow_name,
        work_pool_name="docker-pool",
        image=DockerImage(
            name=f"nexus4shashank/mlopszoomcamp:{flow_name}",
            dockerfile="prefect_base_dockerfile",
        )
    )