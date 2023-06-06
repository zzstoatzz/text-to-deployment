import subprocess
from pathlib import Path
from typing_extensions import Self

from marvin import ai_fn, ai_model
from prefect import Flow
from prefect.client.schemas.schedules import SCHEDULE_TYPES
from prefect.utilities.asyncutils import sync_compatible
from prefect.utilities.importtools import import_object
from pydantic import BaseModel, Field


@ai_fn(llm_model="gpt-4")
def script_to_prefect_flow(script_src: str) -> str:
    """Convert a script to a Prefect flow script.
    
    Must include everything needed to run the script.
    The script should end with an `if __name__ == "__main__"` block
    that calls the `@flow` decorated function, the main entrypoint.
    In Prefect 2, there is NO `with Flow() as flow` syntax, or a public
    `.run()` method on flows. There are only decorated python functions,
    the `with Flow()` syntax is NOT VALID in Prefect 2.
    
    Important pieces of work should be broken into @task-decorated functions IF
    not easily represented as a single function, the main flow should call those functions.
    
    For example:
    
    ```python
    def get_eth_price():
        import httpx
        response = httpx.get('https://api.coinbase.com/v2/prices/ETH-USD/spot')
        price = response.json()['data']['amount']
        print(f'ETH price in USD: {price}')
    ```
    
    could be converted to:
    
    ```python
    from prefect import flow
    
    @flow(log_prints=True)
    def get_eth_price():
        import httpx
        response = httpx.get('https://api.coinbase.com/v2/prices/ETH-USD/spot')
        price = response.json()['data']['amount']
        print(f'ETH price in USD: {price}')
        
    if __name__ == "__main__":
        get_eth_price()
    ```
    """

@ai_model(personality="you are an expert python developer")
class PrefectDeployment(BaseModel):
    """A Prefect deployment."""
    name: str = Field(
        ...,
        description="The name of the deployment.",
        example="a-slugified-name-for-the-deployment",
    )

    description: str = Field(
        ...,
        description="The description of the deployment.",
    )

    entrypoint: Path = Field(
        ...,
        description=(
            "The full path to the flow-decorated function object, relative to the project root."
        ),
        example="flows/flow_file.py:flow_function",
    )
    
    parameters: dict[str, str] = Field(
        default_factory=dict,
        description="Default parameters for the flow.",
        example={"param1": "value1", "param2": "value2"},
    )
    
    schedule: SCHEDULE_TYPES | None = Field(
        None,
        description="The schedule for the deployment, if any.",
    )
    
    @property
    def flow_object(self) -> Flow:
        return import_object(str(self.entrypoint))
    
    @classmethod
    def from_script(cls, filepath: str) -> Self:
        src_path = Path(filepath)
        
        script_text = src_path.read_text()
        flow_file_text = script_to_prefect_flow(script_text)
        flow_file = Path("flows") / src_path.name
        
        flow_file.write_text(flow_file_text)
        
        return cls(
            f"wrote flow to {flow_file!r}:"
            f" {flow_file_text}"
        )

    @sync_compatible
    async def deploy(self):        
        subprocess.run(
            f"prefect deploy {str(self.entrypoint)}", shell=True, check=True
        )
    
if __name__ == "__main__":
    import marvin
    marvin.settings.llm_model = "gpt-4"
    
    deployment = PrefectDeployment.from_script("scripts/heaviest_pokemon.py")
    
    deployment.deploy()
