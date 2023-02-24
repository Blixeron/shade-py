import aiohttp

async def get_json(link, headers=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(link, headers=headers) as resp:
            return await resp.json()