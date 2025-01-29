
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
    url = 'https://bbr.ru/'
    driver.get(url)
    time.sleep(2)

# Получение HTML-кода страницы
    page_source = driver.page_source

    # Парсинг с помощью BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    currency_elements = soup.find_all('span', class_='css-11ctayd exmh6wy0')

    result = []
    if len(currency_elements) >= 8:
        dollar_buy = currency_elements[1].text.strip()
        dollar_buy = dollar_buy.replace(',', '.')
        euro_buy = currency_elements[3].text.strip()
        euro_buy = euro_buy.replace(',', '.')
        yuan_buy = currency_elements[5].text.strip()
        yuan_buy = yuan_buy.replace(',', '.')
        hundred_yen_buy = currency_elements[7].text.strip()
        hundred_yen_buy = hundred_yen_buy.replace(',', '.')
        print(f"Курс покупки доллара: {dollar_buy} руб.")
        print(f"Курс покупки евро: {euro_buy} руб.")
        print(f"Курс покупки юаня: {yuan_buy} руб.")
        print(f"Курс покупки 100 йен: {hundred_yen_buy} руб.")
    else:
        print("Не удалось найти все курсы валют.")
    url = 'https://cbr.ru/currency_base/daily/'
    driver.get(url)
    time.sleep(2)
    page_source = driver.page_source
    # Парсинг с помощью BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')
    rows = soup.find_all("tr")

    for row in rows:
        cols = row.find_all("td")

        if len(cols) >= 5:  # Проверяем, что в строке достаточно данных
            currency_code = cols[0].text.strip()
            if currency_code == "410":
                exchange_rate = cols[4].text.strip()  # Курс валюты
                exchange_rate = exchange_rate.replace(',', '.')
                print(f"Курс покупки 1000 вон : {exchange_rate} руб.")
                break

    result.append({'USD': float(dollar_buy),'EUR': float(euro_buy),'CNY': float(yuan_buy),'JPY': float(hundred_yen_buy) / 100,'KRW': float(exchange_rate) / 1000})
finally:
    driver.quit()
with open(os.path.dirname(__file__) + '/bank_course.json', 'w') as file:
    json.dump(result[0], file)
