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
        for i in pagen:
            async with session.get(url=i) as r1:
                print(i)
                links = [name['href'] for name in BeautifulSoup(await r1.text(), 'lxml').find_all('a', class_='name_item')]
                for j in links:
                    async with session.get(url=f'https://parsinger.ru/html/{j}') as r2:
                        items.append(*[int(art.text.split()[1]) for art in BeautifulSoup(await r2.text(), 'lxml').find_all('p', class_='article')])
        print(sum(items))
        print('finished')


if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

asyncio.run(main())