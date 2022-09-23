from aiocsv import AsyncWriter
import aiofiles
import aiohttp
import asyncio
from bs4 import BeautifulSoup
from typing import List, Tuple


# 1 ------------------------------------------------------
async def create_file(filename: str = 'res') -> None:
    async with aiofiles.open(f'{filename}.csv', 'w', encoding='utf-8-sig', newline='') as file:
        writer = AsyncWriter(file, delimiter=';')
        await writer.writerow([
            'Наименование', 'Цена', 'Бренд', 'Тип', 'Подключение', 'Игровая'])
# 1 ------------------------------------------------------


# 2 ------------------------------------------------------
async def request_data(url: str) -> BeautifulSoup:
    async with aiohttp.ClientSession() as session:
        async with session.get(url=url) as r:
            return BeautifulSoup(await r.text(encoding='utf-8'), 'lxml')

# 2 ------------------------------------------------------


# 3 ------------------------------------------------------
def parse_soup(soup) -> Tuple[list[str], list[str], list[str]]:
    name = [x.text.strip() for x in soup.find_all('a', class_='name_item')]
    description = [x.text.split('\n') for x in soup.find_all('div', class_='description')]
    price = [x.text for x in soup.find_all('p', class_='price')]
    print(name, description, price)
    return name, description, price
# 3 ------------------------------------------------------


# 4------------------------------------------------------
async def write_data(name: List[str], description: List[str], price: List[str], filename: str = 'res') -> None:
    async with aiofiles.open(f'{filename}.csv', 'a', encoding='utf-8-sig', newline='') as file:
        for item, price, descr in zip(name, price, description):
            flatten = item, price, *[x.split(':')[1].strip() for x in descr if x]
            writer = AsyncWriter(file, delimiter=';')
            await writer.writerow(flatten)
    print('Файл res.csv создан')


async def main(url,
               file_name):
    await create_file(file_name)
    soup = await request_data(url)
    tpl = parse_soup(soup)
    await write_data(*tpl,
                     file_name)


if __name__ == '__main__':
    url = 'http://parsinger.ru/html/index3_page_2.html'
    file_name = 'res'
    asyncio.run(main(url, file_name))
