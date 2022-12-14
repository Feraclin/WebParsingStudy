import sys
from pprint import pprint

import aiohttp
import asyncio
from bs4 import BeautifulSoup


async def main():
    async with aiohttp.ClientSession() as session:
        url = 'https://parsinger.ru/html/index3_page_1.html'
        async with session.get(url=url) as r:
            soup2 = BeautifulSoup(await r.text(), 'lxml')
            shema = 'https://parsinger.ru/html/index3_page_'
            pagen = [shema + link.text + '.html' for link in soup2.find('div', class_='pagen').find_all('a')]
            items = []
            print(pagen)
        for i in pagen:
            async with session.get(url=i) as r1:
                print(i)
                items.append([name.text for name in BeautifulSoup(await r1.text(), 'lxml').find_all('a', class_='name_item')])
        print(items)
        print('finished')


if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

asyncio.run(main())