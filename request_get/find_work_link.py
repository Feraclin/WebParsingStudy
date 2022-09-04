import sys

import aiohttp
from aiohttp.web_exceptions import HTTPException
import asyncio


async def request(x: int):
    async with aiohttp.ClientSession() as session:
        url = f'https://parsinger.ru/task/1/{x}.html'
        async with session.get(url=url) as r:
            if r.status == 200:
                with open('output.txt', 'w') as file:
                    file.write(await r.text())


async def main():
    chunk = 100
    tasks = []
    pended = 0

    for x in range(1, 501):
        tasks.append(asyncio.create_task(request(x=x)))
        pended += 1
        if len(tasks) == chunk or pended == 501:
            await asyncio.gather(*tasks)
            tasks = []


if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

asyncio.run(main())
