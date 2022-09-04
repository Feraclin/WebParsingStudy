import sys

import aiohttp
import asyncio


async def main():
    async with aiohttp.ClientSession() as session:
        url = 'http://parsinger.ru/video_downloads/videoplayback.mp4'
        async with session.get(url=url) as r:
            with open('file.mp4', 'wb') as file:
                async for data in r.content.iter_chunked(1024):
                    file.write(data)
        print('finished')


if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

asyncio.run(main())
