# /// script
# dependencies = ["prefect"]
# ///

"""
A simple flow that says hello.
"""

from prefect import flow, get_run_logger, tags


# The name of the flow, `hello` is inferred from the function name by default
# The arguments to the flow are type annotated and Prefect will validate them at runtime
@flow
def hello(name: str = "Marvin"):
    get_run_logger().info(f"Hello, {name}!")

if __name__ == "__main__":
    flow_name = "hello-world-flow"
    hello.deploy(
        name=flow_name,
        work_pool_name="docker-pool",
        image=f"nexus4shashank/mlopszoomcamp:{flow_name}"
    )