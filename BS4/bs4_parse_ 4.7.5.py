import sys
from pprint import pprint

import aiohttp
import asyncio
from bs4 import BeautifulSoup


async def main():
    async with aiohttp.ClientSession() as session:
        url = 'https://parsinger.ru/table/4/index.html'
        async with session.get(url=url) as r:
            soup2 = BeautifulSoup(await r.text(), 'lxml')

            items = [item.text for item in soup2.find_all('td', class_='green')]
        pprint(items)
        pprint(sum(map(float, items)))
        print('finished')


if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

asyncio.run(main())