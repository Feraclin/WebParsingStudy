import sys
from pprint import pprint

import aiohttp
import asyncio
from bs4 import BeautifulSoup


async def main():
    async with aiohttp.ClientSession() as session:
        url = 'https://parsinger.ru/table/5/index.html'
        async with session.get(url=url) as r:
            soup2 = BeautifulSoup(await r.text(), 'lxml')

            items = [item.text.strip().split('\n') for item in soup2.find_all('tr')]
        dct = dict(zip(items[0], map(lambda x: (sum(map(float, x))), __import__('numpy').transpose(items[1:]))))
        [print(f"{k}: {v: .2f}" for k, v in dct.items()]
        print('finished')


if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

asyncio.run(main())
