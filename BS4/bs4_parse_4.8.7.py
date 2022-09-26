from datetime import datetime
from aiocsv import AsyncWriter
import aiofiles
import aiohttp
import asyncio
import logging
from bs4 import BeautifulSoup
from typing import List


logging.basicConfig(level=logging.INFO)


async def create_file(filename: str = 'res') -> None:
    async with aiofiles.open(f'{filename}.csv', 'w', encoding='utf-8-sig', newline='') as file:
        writer = AsyncWriter(file, delimiter=';')
        await writer.writerow([
            'Наименование', 'Артикул', 'Бренд', 'Модель', 'Наличие', ' Цена', 'Старая цена', 'Ссылка на карточку с товаром'
        ])


async def request_data(url: str) -> BeautifulSoup:
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as r:
            logging.info(f'Parse {url} at {datetime.now()}')
            return BeautifulSoup(await r.text(encoding='utf-8'), 'lxml')


async def parse_soup(name: List[str | None],
                     art: List[str | None],
                     description: List[List[str] | None],
                     stock: List[str | None],
                     price: List[str | None],
                     old_price: List[str | None],
                     urls: List[str | None],
                     url: str) -> None:
    soup = await request_data(url)
    name.append(soup.find('p', id='p_header').text.strip())
    art.append(soup.find('p', class_='article').text.strip().split()[1])
    description.append(soup.find('ul', id='description').text.split('\n'))
    stock.append(soup.find('span', id='in_stock').text.strip().split()[2])
    price.append(soup.find('span', id='price').text.strip())
    old_price.append(soup.find('span', id='old_price').text.strip())
    urls.append(url)


async def write_data(name: List[str],
                     art: List[str],
                     description: List[List[str]],
                     stock: List[str],
                     price: List[str],
                     old_price: List[str],
                     urls: List[str],
                     link: str,
                     filename: str = 'res') -> None:
    async with aiofiles.open(f'{filename}.csv', 'a', encoding='utf-8-sig', newline='') as file:
        for item, art_, descr, stock_, price_, old_price_, url in zip(name, art, description, stock, price, old_price, urls):
            flatten = item, art_, *[x.split(':')[1].strip() for x in descr if x][:2], stock_,  price_, old_price_, url
            writer = AsyncWriter(file, delimiter=';')
            await writer.writerow(flatten)
    logging.info(f'Файл создан для ссылки {link} at {datetime.now()}')


async def main(url,
               filename):
    tasks = []
    await create_file(filename)

    soup = await request_data(url + 'index1_page_1.html')
    category = [f'{link.get("href")}' for link in soup.find('div', class_='nav_menu').find_all('a')]
    pagen = []

    for link in category:
        soup = await request_data(url + link)
        pagen.extend([f'{link.get("href")}' for link in soup.find('div', class_='pagen').find_all('a')])

    links = [f'{link.get("href")}' for lnk in pagen for link in (await request_data(url + lnk)).find_all('a', class_='name_item')]

    name, art, description, stock, price, old_price, urls = [], [], [], [], [], [], []

    for link in links:
        tasks.append(asyncio.create_task(parse_soup(name=name,
                                                    art=art,
                                                    description=description,
                                                    stock=stock,
                                                    price=price,
                                                    old_price=old_price,
                                                    urls=urls,
                                                    url=url + link)))

    await asyncio.gather(*tasks)

    await write_data(name=name,
                     art=art,
                     description=description,
                     stock=stock,
                     price=price,
                     old_price=old_price,
                     urls=urls,
                     link=url,
                     filename=filename)

if __name__ == '__main__':
    url_host = 'https://parsinger.ru/html/'
    out_file_name = 'result_all_cat'
    asyncio.run(main(url_host, out_file_name))
