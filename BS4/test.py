from bs4 import BeautifulSoup
import requests
import csv

url = "https://parsinger.ru/html/index1_page_1.html"
headers = [
    'Наименование', 'Артикул', 'Бренд', 'Модель', 'Наличие', 'Цена',
    'Старая цена', 'Ссылка на карточку с товаром'
]

response = requests.get(url)
response.encoding = "utf-8"
soup = BeautifulSoup(response.text, "lxml")

pages = int(soup.find('div', class_="pagen").find_all('a')[-1].text)
categories = [
    tag['href'] for tag in soup.find('div', class_="nav_menu").find_all('a')
]

with open("res.csv", 'w', encoding="utf-8-sig", newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(headers)
    for i in range(1, len(categories) + 1):
        for j in range(1, pages + 1):
            url = f"https://parsinger.ru/html/index{i}_page_{j}.html"
            response = requests.get(url)
            response.encoding = "utf-8"
            soup = BeautifulSoup(response.text, "lxml")
            for tag in soup.find_all('a', class_="name_item"):
                link = "https://parsinger.ru/html/" + tag["href"]
                response = requests.get(link)
                response.encoding = "utf-8"
                soup = BeautifulSoup(response.text, "lxml")
                name = soup.find('p', id="p_header").text
                article = soup.find('p', class_="article").text.split(':')[-1]
                params = [
                    li.text.split(':')[-1].strip() for li in soup.find(
                        'ul', id="description").find_all('li')[:2]
                ]
                count = int(
                    soup.find('span',
                              id="in_stock").text.split(':')[-1].strip())
                price = soup.find('span', id="price").text
                old_price = soup.find('span', id="old_price").text
                writer.writerow(
                    [name, article, *params, count, price, old_price, link])