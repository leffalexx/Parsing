# Выберите веб-сайт с табличными данными, который вас интересует.
# Напишите код Python, использующий библиотеку requests для отправки HTTP GET-запроса на сайт и получения HTML-содержимого страницы.
# Выполните парсинг содержимого HTML с помощью библиотеки lxml, чтобы извлечь данные из таблицы.
# Сохраните извлеченные данные в CSV-файл с помощью модуля csv.

# Ваш код должен включать следующее:

# Строку агента пользователя в заголовке HTTP-запроса, чтобы имитировать веб-браузер и избежать блокировки сервером.
# Выражения XPath для выбора элементов данных таблицы и извлечения их содержимого.
# Обработка ошибок для случаев, когда данные не имеют ожидаемого формата.
# Комментарии для объяснения цели и логики кода.

import requests
from lxml import html
from pymongo import MongoClient
import json
import csv

url = 'https://listmuse.com/best-books-top-100-fiction.php'
page = requests.get(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
})

tree = html.fromstring(page.content)

#Найдем таблицу с книгами в html разметке:
books = tree.xpath("//div[@class='col-md-9']/div[@class='container']/div[@class='row']")

top_100_books = []

# Пройдемся циклом потаблице, обрабатывая ошибки:
for i in books:
    try:
        rank = int(i.xpath(
            ".//div[@class='col-md-9 col-xs-7 ']/h2/text()")[0].strip('. '))
    except ValueError:
        rank = None
    try:
        book = i.xpath(".//div[@class='col-md-9 col-xs-7 ']/h2/a/text()")[0]
    except IndexError:
        book = None
    try:
        author = i.xpath(".//div[@class='col-md-9 col-xs-7 ']/p/a/text()")[0]
    except IndexError:
        author = None

    data = {
        'rank': rank,
        'book': book,
        'author': author
    }
    top_100_books.append(data)

# Сохраним json:
with open('top_100_books.json', 'w') as f:
    json.dump(top_100_books, f)

# Сохраним в csv:
with open('top_100_books.csv', 'w', newline='') as csvfile:
    fieldnames = ['rank', 'book', 'author']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for row in top_100_books:
        writer.writerow(row)

# Загрузим данные в уже созданную БД 'booksdb', создав новую коллекцию:
client = MongoClient('mongodb://localhost:27017/')
db = client['booksdb']
collection = db['top_100_books']

try:
    collection.insert_many(top_100_books)
    print("Данные успешно загружены!")
except Exception as e:
    print("Ошибка при загрузке данных: ", e)

print(f'В коллекции {collection.name} теперь {collection.count_documents({})} книг')
