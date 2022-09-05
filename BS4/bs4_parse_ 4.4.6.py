import sys
from pprint import pprint

import aiohttp
import asyncio
from bs4 import BeautifulSoup


async def main():
    async with aiohttp.ClientSession() as session:
        url = 'http://parsinger.ru/html/index1_page_1.html'
        async with session.get(url=url) as r:
            with open('index.html', 'r', encoding='utf-8') as file:
                soup2 = BeautifulSoup(file, 'lxml')
                price_lst = soup2.find_all('p', class_='price')
                pprint(sum([int(i.text.split()[0]) for i in price_lst]))
        print('finished')


if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

asyncio.run(main())