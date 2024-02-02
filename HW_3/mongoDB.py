import json
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['booksdb']
collection = db['books']

with open('data.json') as f:
  data = json.load(f)

print(f"Загружается {len(data)} книг...")

try:
  collection.insert_many(data)
  
  print("Данные успешно загружены!")
  
except Exception as e:
  print("Ошибка при загрузке данных: ", e)
  
print(f'В коллекции {collection.name} теперь {collection.count_documents({})} книг')
