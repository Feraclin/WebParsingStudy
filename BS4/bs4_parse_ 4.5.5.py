import sys
from pprint import pprint

import aiohttp
import asyncio
from bs4 import BeautifulSoup


link = []
items = []

async def request_link(url: str, sheme: str) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as r:
            soup2 = BeautifulSoup(await r.text(), 'lxml')

            pagen = [f'{sheme}{link.text}.html' for link in soup2.find('div', class_='pagen').find_all('a')]
        for i in pagen:
            async with session.get(url=i) as r1:
                link.extend([name['href'] for name in BeautifulSoup(await r1.text(), 'lxml').find_all('a', class_='name_item')])
        print('finished')


async def request_price(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as r:
            price = ([int(name.text.split()[0]) for name in BeautifulSoup(await r.text(), 'lxml').find_all('span', id='price')])
            count = ([int(name.text.split()[2]) for name in BeautifulSoup(await r.text(), 'lxml').find_all('span', id='in_stock')])
            items.extend([i * j for i in price for j in count])


async def main():
    tasks = []



    for x in range(1, 6):
        tasks.append(asyncio.create_task(request_link(url=f'https://parsinger.ru/html/index{x}_page_1.html', sheme=f'https://parsinger.ru/html/index{x}_page_')))

    await asyncio.gather(*tasks)
    tasks = []

    for i in link:
        tasks.append(asyncio.create_task(request_price(url=f'https://parsinger.ru/html/{i}')))

    await asyncio.gather(*tasks)

    print(len(items))
    pprint(sum(items))




if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

asyncio.run(main())