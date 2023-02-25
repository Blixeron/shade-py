import aiohttp

async def get_json(link: str, headers: dict = None):
    async with aiohttp.ClientSession() as session:
        async with session.get(link, headers=headers) as resp:
            return await resp.json()