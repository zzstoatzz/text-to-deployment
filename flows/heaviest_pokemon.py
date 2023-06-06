from prefect import flow, task

@task
async def get_heaviest_pokemon(n: int = 5, limit: int = 100):
    import asyncio
    import httpx

    async with httpx.AsyncClient() as client:
        pokemon = [client.get(f"https://pokeapi.co/api/v2/pokemon/{i}") for i in range(1, limit)]
        sorted_pokemon = sorted(
            [p.json() for p in await asyncio.gather(*pokemon)],
            key=lambda p: p['weight'],
            reverse=True
        )
        
    for i, p in enumerate(sorted_pokemon[:n]):
        print(f"{i+1}. {p['name'].capitalize()} (Weight: {p['weight']})")

@flow(log_prints=True)
def main_flow():
    get_heaviest_pokemon()

if __name__ == "__main__":
    main_flow()