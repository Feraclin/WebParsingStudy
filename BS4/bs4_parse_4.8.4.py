from datetime import datetime
from aiocsv import AsyncWriter
import aiofiles
import aiohttp
import asyncio
import logging
from bs4 import BeautifulSoup
from typing import List, Tuple


logging.basicConfig(level=logging.INFO)


async def create_file(filename: str = 'res') -> None:
    async with aiofiles.open(f'{filename}.csv', 'w', encoding='utf-8-sig', newline='') as file:
        writer = AsyncWriter(file, delimiter=';')
        await writer.writerow([
            'Наименование', 'Бренд', 'Форм-фактор', 'Ёмкость', 'Объём буф. памяти', 'Цена',
        ])


async def request_data(url: str) -> BeautifulSoup:
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as r:
            logging.info(f'Parse {url} at {datetime.now()}')
            return BeautifulSoup(await r.text(encoding='utf-8'), 'lxml')


def parse_soup(soup) -> Tuple[list[str], list[str], list[str]]:
    name = [x.text.strip() for x in soup.find_all('a', class_='name_item')]
    description = [x.text.split('\n') for x in soup.find_all('div', class_='description')]
    price = [x.text for x in soup.find_all('p', class_='price')]
    return name, description, price


async def write_data(name: List[str], description: List[str], price: List[str], link: str, filename: str = 'res') -> None:
    async with aiofiles.open(f'{filename}.csv', 'a', encoding='utf-8-sig', newline='') as file:
        for item, descr, price in zip(name, description, price,):
            flatten = item, *[x.split(':')[1].strip() for x in descr if x], price
            writer = AsyncWriter(file, delimiter=';')
            await writer.writerow(flatten)
    logging.info(f'Файл res.csv создан для ссылки {link} at {datetime.now()}')


async def main(url,
               filename):
    tasks = []
    await create_file(filename)
    soup = await request_data(url + 'index4_page_1.html')
    pagen = [f'{link.get("href")}' for link in soup.find('div', class_='pagen').find_all('a')]
    logging.info(f'Pages: {pagen}')
    for link in pagen:
        tasks.append(asyncio.create_task(write_data(*parse_soup(soup=await request_data(url + link)),
                                                    link=link,
                                                    filename=filename)))
    logging.info(f'tasks {datetime.now()}')
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    url_host = 'https://parsinger.ru/html/'
    out_file_name = 'result'
    asyncio.run(main(url_host, out_file_name))
