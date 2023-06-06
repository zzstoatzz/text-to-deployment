import asyncio
import httpx

async def get_heaviest_pokemon(limit: int = 100):
    async with httpx.AsyncClient() as client:
        pokemon = [client.get(f"https://pokeapi.co/api/v2/pokemon/{i}") for i in range(1, limit)]
        sorted_pokemon = sorted(
            [p.json() for p in await asyncio.gather(*pokemon)],
            key=lambda p: p['weight'],
            reverse=True
        )
        
    for i, p in enumerate(sorted_pokemon[:5]):
        print(f"{i+1}. {p['name'].capitalize()} (Weight: {p['weight']})")

if __name__ == "__main__":
    asyncio.run(get_heaviest_pokemon())
