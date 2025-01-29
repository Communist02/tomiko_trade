
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
    time.sleep(5)

# Получение HTML-кода страницы
    page_source = driver.page_source

    # Парсинг с помощью BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    currency_elements = soup.find_all('span', class_='css-11ctayd exmh6wy0')

    result = []
    if len(currency_elements) >= 8:
        dollar_buy = currency_elements[1].text.strip()
        dollar_buy = dollar_buy.replace(',', '.')
        result.append({'dollar': float(dollar_buy)})
        euro_buy = currency_elements[3].text.strip()
        euro_buy = euro_buy.replace(',', '.')
        result.append({'EURO': float(euro_buy)})
        yuan_buy = currency_elements[5].text.strip()
        yuan_buy = yuan_buy.replace(',', '.')
        result.append({'yuan': float(yuan_buy)})
        hundred_yen_buy = currency_elements[7].text.strip()
        hundred_yen_buy = hundred_yen_buy.replace(',', '.')
        result.append({'100_yen': float(hundred_yen_buy)/100})
        von1000_buy = 68.38/1000
        result.append({'1000_von': von1000_buy})
        print(f"Курс покупки доллара: {dollar_buy} руб.")
        print(f"Курс покупки евро: {euro_buy} руб.")
        print(f"Курс покупки юаня: {yuan_buy} руб.")
        print(f"Курс покупки 100 йен: {hundred_yen_buy} руб.")
        print(f"Курс покупки 1000 вон: {von1000_buy} руб.")
    else:
        print("Не удалось найти все курсы валют.")

finally:
    driver.quit()
with open(os.path.dirname(__file__) + '/bank_course.json', 'w') as file:
    json.dump(result, file)
