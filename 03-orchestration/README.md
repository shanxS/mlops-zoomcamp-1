### what?
Notes to schedule Prefect wf using locally running docker-pool

### Notes
0. To setup local docker-pool, just have docker daemon accessible and follow the instructions. I might have used the cmd line wizard. `prefect-docker` and `prefect` pkg versions need to play well. To start the pool use `prefect worker start --pool docker-pool`
1. `p deployment` gives options but probably not the best way. You want to create a image and then point that for deployment
2. THe version of `hello_world.py` checked in with this creates an image, pushes it to [docker hub](https://hub.docker.com/repository/docker/nexus4shashank/mlopszoomcamp/general) & then schedules. [Doc link](https://docs.prefect.io/v3/deploy/infrastructure-examples/docker#automatically-bake-your-code-into-a-docker-image)

### cmd dump
```bash
alias p='uv run -- prefect'
docker login -u nexusshashank
uv run -- python hello_world.py 
```