from datetime import datetime

from aiocsv import AsyncWriter
import aiofiles
import aiohttp
import asyncio
import logging
from bs4 import BeautifulSoup
from typing import List


logging.basicConfig(level=logging.INFO)


async def request_data(url: str) -> BeautifulSoup:
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as r:
            logging.info(f'Parse {url} at {datetime.now()}')
            return BeautifulSoup(await r.text(encoding='utf-8'), 'lxml')


async def parse_soup(name, description, price, url) -> None:
    soup = await request_data(url)
    name.extend([x.text.strip() for x in soup.find_all('a', class_='name_item')])
    description.extend([x.text.split('\n') for x in soup.find_all('div', class_='description')])
    price.extend([x.text for x in soup.find_all('p', class_='price')])


async def write_data(name: List[str], description: List[str], price: List[str], link: str, filename: str = 'res') -> None:
    async with aiofiles.open(f'{filename}.csv', 'w', encoding='utf-8-sig', newline='') as file:
        for item, descr, price in zip(name, description, price,):
            flatten = item, *[x.split(':')[1].strip() for x in descr if x], price
            print(flatten)
            writer = AsyncWriter(file, delimiter=';')
            await writer.writerow(flatten)
    logging.info(f'Файл создан для ссылки {link} at {datetime.now()}')


async def main(url,
               filename):
    tasks = []
    soup = await request_data(url + 'index1_page_1.html')
    category = [f'{link.get("href")}' for link in soup.find('div', class_='nav_menu').find_all('a')]
    pagen = []
    for link in category:
        soup = await request_data(url + link)
        pagen.extend([f'{link.get("href")}' for link in soup.find('div', class_='pagen').find_all('a')])

    name, description, price = [], [], []

    for link in pagen:
        tasks.append(asyncio.create_task(parse_soup(name, description, price, url + link)))

    await asyncio.gather(*tasks)

    await write_data(name, description, price, url, filename)

if __name__ == '__main__':
    url_host = 'https://parsinger.ru/html/'
    out_file_name = 'result_all'
    asyncio.run(main(url_host, out_file_name))
