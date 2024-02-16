from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import time
import json
import csv
import requests

driver = webdriver.Chrome()

heritagesites = []

driver.get("https://www.unesco.org/en/world-heritage/list")
time.sleep(5)

elements = driver.find_elements(
    By.XPATH, "//a[@class='row mt-4 text-decoration-none node unesco-type--structured_data teaser']")

for el in elements:

    actions = ActionChains(driver)
    actions.move_to_element_with_offset(el, 5, 5)
    actions.click()
    actions.perform()

    time.sleep(1)

    # Убедимся, что получаем корректный ответ от сайта
    if requests.get(driver.current_url).status_code != 200:
        print(f"Ошибка: Не удалось загрузить страницу {driver.current_url}")
        break

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Обработка ошибок при парсинге данных
    try:
        name = soup.find('h1').text.strip()
        country = soup.find('div', class_='d-flex mb-3').text.strip()
        coords_block = soup.find('div', class_='mt-3 small text-muted')
        if len(coords_block.find_all('div')) > 1:
            coordinates = coords_block.find_all('div')[1].text.strip()
        else:
            coordinates = coords_block.text.strip()
    except AttributeError as e:
        print(f"Ошибка при извлечении данных: {e}")
        continue

    data = [name, country, coordinates]

    heritagesites.append(data)

    # Сохранение данных в JSON файл
    try:
        with open('heritagesites.json', 'w', encoding='utf-8') as f:
            json.dump(heritagesites, f, ensure_ascii=False)
    except IOError as e:
        print(f"Ошибка при записи в JSON файл: {e}")

    try:
        with open('heritagesites.csv', 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Name', 'Country', 'Coordinates'])
            csv_writer.writerows(heritagesites)
    except IOError as e:
        print(f"Ошибка при записи в CSV файл: {e}")

    driver.back()

driver.quit()

print("Готово")
