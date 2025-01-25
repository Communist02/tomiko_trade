import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
import json

# Настройка браузера Firefox
firefox_options = Options()
firefox_options.add_argument("--headless")  # Фоновый режим

# Укажите путь к вашему geckodriver
service = Service('/path/to/geckodriver')  # Замените на ваш путь

# Запуск браузера
driver = webdriver.Firefox(options=firefox_options)
try:
    # URL страницы с клипами
    url = 'https://vk.com/clips/tomiko_trade'
    driver.get(url)

    # Ожидание загрузки страницы
    time.sleep(5)  # Увеличьте, если контент загружается долго

    # Получение HTML-кода страницы
    page_source = driver.page_source

    # Парсинг с помощью BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Поиск всех элементов клипов
    clips = soup.find_all('a', {'data-testid': 'clip-preview'}, limit=10)  # Ограничиваем до 10 элементов

    # Сбор данных в массив
    result = []
    for clip in clips:
        href = clip.get('href')  # Ссылка на клип
        img_tag = clip.find('img')  # Превью
        img_src = img_tag.get('src') if img_tag else 'No image'

        # Добавляем в массив
        result.append({'href': url + href, 'preview': img_src})

    # Вывод результата
    for item in result:
        print(f"Ссылка: {item['href']}, Превью: {item['preview']}")

finally:
    # Закрытие браузера
    driver.quit()

with open(os.path.dirname(__file__) + '/vk.json', 'w') as file:
    json.dump(result, file)