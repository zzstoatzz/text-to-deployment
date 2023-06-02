import subprocess
from typing import Optional

import marvin
from marvin import ai_model
from prefect import flow
from prefect.deployments import Deployment
from prefect.server.schemas.schedules import CronSchedule
from pydantic import BaseModel, Field, validator

def get_function_from_string(func_str: str) -> callable:
    local_namespace = {}
    exec(func_str, local_namespace)
    
    for _, obj in local_namespace.items():
        if callable(obj):
            return obj

@ai_model(personality="you are an expert python developer")
class PrefectDeployment(BaseModel):
    """A Prefect deployment that is created from a natural language description.
    
    A schedule should only be populated if the user describes a recurring task.
    """
    python_function: str = Field(
        description=(
            "The source code for a python function that accomplishes a goal."
            " This function should be named according to the desired outcome."
            " This string should only contain a valid python function."
        ),
    )
    name: str = Field(
        description="A slugified name for the deployment.",
    )
    description: str = Field(
        description="A description of what the function does.",
    )
    schedule: Optional[CronSchedule] = Field(
        None,
        description="A optional cron schedule for the flow to run on.",
    )
    
    def write_flow_to_file(self):
        """Write the flow to a file."""
        with open(f"flows/{self.name}.py", "w") as f:
            f.write("@flow\n"+self.python_function)
    
if __name__ == "__main__":
    
    marvin.settings.openai_model_name = "gpt-4"
    
    deployment = PrefectDeployment(
        "I want to see the price of ETH in USD every 5 minutes.",
    )
    
    deployment.write_flow_to_file()
    
    subprocess.run(
        [
            "prefect",
            "deploy",
            f"{deployment.name}.py:{deployment.name}",
            "-n",
            f"{deployment.name}",
            "-p",
            "kubernetes-prd-internal-tools",
        ]
    )

