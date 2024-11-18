import json
import requests
import aiohttp
import asyncio

async def fetch_data(url, data: dict, headers: dict, params: dict):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, json=data, params=params) as response:
            return await response.json()  


async def main():
    response = await fetch_data("http://172.16.100.200:4000/song/url", data=None, headers=None, params={"id":"27646992"})
    print(response)


#if __name__ == '__main__':
    asyncio.run(main())
