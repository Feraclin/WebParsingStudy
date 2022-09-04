import sys

import aiohttp
import asyncio


async def request(x: int):
    async with aiohttp.ClientSession() as session:
        url = f'http://parsinger.ru/img_download/img/ready/{x}.png'
        async with session.get(url=url) as r:
            print(x)
            with open(f'img/{x}.png', 'wb') as file:
                async for data in r.content.iter_chunked(1024):
                    file.write(data)


async def main():
    chunk = 160
    tasks = []
    pended = 0

    for x in range(1, 161):
        tasks.append(asyncio.create_task(request(x=x)))
        pended += 1
        if len(tasks) == chunk or pended == 501:
            await asyncio.gather(*tasks)
            tasks = []


if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

asyncio.run(main())
