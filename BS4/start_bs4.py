from bs4 import BeautifulSoup

with open('index.html', 'r', encoding='utf-8') as file:
    soup2 = BeautifulSoup(file, 'lxml')
    print(soup2)
