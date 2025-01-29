import os
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
import time
import json
#from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
#from selenium.webdriver.firefox.options import Options
import time

# Настройка браузера Firefox
firefox_options = Options()
firefox_options.add_argument("--headless")  # Фоновый режим

# Укажите путь к вашему geckodriver
service = Service('/path/to/geckodriver')  # Замените на ваш путь

# Запуск браузера
driver = webdriver.Firefox(options=firefox_options)

try:
    # URL страницы с клипами
    url = 'https://yandex.ru/maps/org/vladivostokskiy_gosudarstvenny_universitet_korpus_3/1033268555/reviews'
    driver.get(url)

    time.sleep(5)  # Ждем загрузки страницы

    # Получение HTML-кода страницы
    page_source = driver.page_source

    # Парсинг с помощью BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    reviews = soup.find_all('div', class_='business-reviews-card-view__review', limit=10)  # Ограничиваем до 10 элементов

    result = []
    for review in reviews:
        # Имя пользователя
        username = review.find('span',itemprop="name",dir="auto").text
        # Текст отзыва
        text = review.find('span', class_='business-review-view__body-text').text
        # Рейтинг отзыва из <meta itemprop="ratingValue">
        rating_meta = review.find('meta',itemprop='ratingValue')
        rating = rating_meta.get('content')
        date = review.find('span', class_='business-review-view__date').text
        result.append({'username': username, 'text': text, 'rating': rating, 'date': date})
finally:
    driver.quit()
# print (result)
with open(os.path.dirname(__file__) + '/yandex_reviews.json', 'w',encoding="utf-8") as file:
    json.dump(result, file, ensure_ascii=False, indent=4)