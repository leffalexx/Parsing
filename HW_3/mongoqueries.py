from pymongo import MongoClient

client = MongoClient()

db = client['booksdb']
collection = db['books']


#Поиск книги по названию и вывод всей информации о ней:
book_by_name = collection.find_one({'name': 'A Light in the Attic'})
print(book_by_name)


#Подсчет количества книг, которых больше 19 в наличии:
qty_filter = {'qty': {'$gt': 19}}
count = collection.count_documents(qty_filter)
print(f'Количество книг больше 19: {count}')


#Расчет общей стоимости всех книг в БД:
pipeline = [
    {
        '$group': {
            '_id': None, 
            'total': {
                '$sum': '$price'
            }
        }
    }
]

result = collection.aggregate(pipeline)

total_sum = 0
for doc in result:
    total_sum = doc['total']
    
print(f'Общая сумма цен книг: {total_sum}')
