import sys
from pprint import pprint

import aiohttp
import asyncio
from bs4 import BeautifulSoup


async def main():
    async with aiohttp.ClientSession() as session:
        url = 'https://parsinger.ru/table/1/index.html'
        async with session.get(url=url) as r:
            soup2 = BeautifulSoup(await r.text(), 'lxml')

            items = [item.text.split('\n')[1] for item in soup2.find_all('tr')]

        pprint(sum(map(float, items[1:])))
        print('finished')


if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

asyncio.run(main())