import aiohttp


async def fetch_anilist(url, query: str, variables: dict) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json={"query": query, "variables": variables}) as resp:
            return await resp.json()

async def fetch_html(url: str) -> str:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()