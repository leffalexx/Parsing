# Выполнить скрейпинг данных в веб-сайта http://books.toscrape.com/ и извлечь информацию о всех книгах на сайте во всех категориях:
# название, цену, количество товара в наличии (In stock (19 available)) в формате integer, описание.
# Затем сохранить эту информацию в JSON-файле.

from bs4 import BeautifulSoup
import requests
import urllib.parse
import re
import json

name = []
price = []
qty = []
content = []
output = {}

baseurl = 'https://books.toscrape.com/catalogue/'
url = baseurl + 'page-1.html'
counter = 2

while True:

    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    next_page_link = soup.find('a', text='next')
    result = soup.find_all('article', ('class', 'product_pod'))

    url_2 = []
    for i in result:
        for link in i.find_all('div', ('class', 'image_container')):
            url_2.append(link.find('a').get('href'))

    url_joined = []

    for link in url_2:
        url_joined.append(urllib.parse.urljoin(baseurl, link))

    for i in url_joined:
        response = requests.get(i)

        soup = BeautifulSoup(response.content, 'html.parser')

        # Парсинг названия товара. Обработка исключения: добавляем пустую строку.
        try:
            name.append(soup.find('h1').text)
        except:
            name.append('')

        # Парсинг цены товара.
        try:
            p = soup.find('p', class_='price_color').text
            p = float(p.replace('£', ''))
            price.append(p)
        except:
            price.append('')

        # Парсинг количества.
        try:
            availability_text = soup.find(
                'p', class_='instock availability').text
        # Используем регулярное выражение для извлечения числа из строки
            qty_match = re.search(r'\((\d+) available\)', availability_text)
            if qty_match:
                qty.append(int(qty_match.group(1)))
            else:
                qty.append('')
        except:
            qty.append('')

        # Парсинг описания.
        try:
            product_description_div = soup.find(
                'div', id='product_description', class_='sub-header')
            if product_description_div:
                description_p = product_description_div.find_next('p')
                if description_p:
                    description = description_p.text.strip()
                    content.append(description)
                else:
                    content.append('')
            else:
                content.append('')
        except:
            content.append('')

        output = {'Name': name, 'Price': price,
                  'Quantity': qty, 'Content': content}

    if not next_page_link:
        break

    url = baseurl + next_page_link['href']
    print(f'Страница каталога {counter} обработана')
    counter+=1


data = []
for i in range(len(name)):
    item = {
        'name': name[i],
        'price': price[i],
        'qty': qty[i],
        'content': content[i]
    }
    data.append(item)

with open('data.json', 'w') as f:
    json.dump(data, f)
