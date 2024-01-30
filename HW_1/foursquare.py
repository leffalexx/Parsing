import requests
import json


client_id = "1FFEXPWQVRWPG5OODTZVLSZ2PGICZU3FKRZQWPVYSYRHCPVL"
client_secret = "54M4V2UKBTVQGDFGGF4V3SWINHJTZXFBHZV5QG03YURDQR2Y"

endpoint = "https://api.foursquare.com/v3/places/search"

city = input("Введите название города: ")
params = {
    "client_id": client_id,
    "client_secret": client_secret,
    "near": city,
    "query": "restaurant"
}

headers = {
    "Accept": "application/json",
    "Authorization": "fsq3PyDppXgErl/5pzaPwMSt0/ofLr5pHgmjdv2Y8Su4B/s="
}

response = requests.get(endpoint, params=params,headers=headers)

if response.status_code == 200:
    print("Успешный запрос API!")
    data = json.loads(response.text)
    venues = data["results"]
    for venue in venues:
        print("Название:", venue["name"])
        print("Адрес:", venue["location"]["address"])
        print("\n")
else:
    print("Запрос API завершился неудачей с кодом состояния:", response.status_code)
    print(response.text)
    