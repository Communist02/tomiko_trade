import json
import os
from django.shortcuts import redirect, render
from .models import Car
from .models import Brand
from .models import Request
from django.db.models.lookups import GreaterThanOrEqual
from django.db.models.lookups import LessThanOrEqual
from django.db.models import F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime

# Create your views here.
def index(request):
    cars = Car.objects.all()[:10]
    with open(os.path.dirname(__file__) + '/modules/bank_course.json', 'r') as file:
        data = json.load(file)

        for i in range(len(cars)):
            if cars[i].brand_country.country == 'Япония':
                koef = data['JPY']
            elif cars[i].brand_country.country == 'Китай':
                koef = data['CNY']
            elif cars[i].brand_country.country == 'США':
                koef = data['USD']
            elif cars[i].brand_country.country == 'Европа':
                koef = data['EUR']
            elif cars[i].brand_country.country == 'Корея':
                koef = data['KRW']
            cars[i].price = int(koef * cars[i].price)
    with open(os.path.dirname(__file__) + '/modules/vk.json', 'r') as file:
        clips = json.load(file)
    return render(request, 'main/index.html', {'pop_cars': cars, 'clips': clips})

def about_us(request):
    return render(request, 'main/about_us.html')

def promo(request):
    return render(request, 'main/promo.html')

def contacts(request):
    return render(request, 'main/contacts.html')

def auto(request):
    sort = request.GET.get('sort')
    brand = request.GET.get('brand')
    drive = request.GET.get('drive')
    color = request.GET.get('color')
    model = request.GET.get('model')
    transmission = request.GET.get('transmission')
    year_from = request.GET.get('year_from')
    year_to = request.GET.get('year_to')
    mileage_from = request.GET.get('mileage_from')
    mileage_to = request.GET.get('mileage_to')
    volume_from = request.GET.get('volume_from')
    volume_to = request.GET.get('volume_to')

    match sort:
        case 'mileage_h':
            cars = Car.objects.order_by('mileage')
        case 'mileage_l':
            cars = Car.objects.order_by('-mileage')
        case 'price_h':
            cars = Car.objects.order_by('price')
        case 'price_l':
            cars = Car.objects.order_by('-price')
        case 'year_h':
            cars = Car.objects.order_by('year')
        case 'year_l':
            cars = Car.objects.order_by('-year')
        case 'volume_h':
            cars = Car.objects.order_by('engine_volume')
        case 'volume_l':
            cars = Car.objects.order_by('-engine_volume')
        case _:
            cars = Car.objects.all()

    if color:
        cars = cars.filter(color=color)
    if brand:
        cars = cars.filter(brand_country=brand)
    if drive:
        cars = cars.filter(drive=drive)
    if model:
        cars = cars.filter(model=model)
    if transmission:
        cars = cars.filter(transmission=transmission)
    if year_from:
        cars = cars.filter(GreaterThanOrEqual(F('year'), year_from))
    if year_to:
        cars = cars.filter(LessThanOrEqual(F('year'), year_to))
    if mileage_from:
        cars = cars.filter(GreaterThanOrEqual(F('mileage'), mileage_from))
    if mileage_to:
        cars = cars.filter(LessThanOrEqual(F('mileage'), mileage_to))
    if volume_from:
        cars = cars.filter(GreaterThanOrEqual(F('engine_volume'), volume_from))
    if volume_to:
        cars = cars.filter(LessThanOrEqual(F('engine_volume'), volume_to))

    pop_cars = Car.objects.all()[:10]

    with open(os.path.dirname(__file__) + '/modules/bank_course.json', 'r') as file:
        data = json.load(file)

        for i in range(len(cars)):
            if cars[i].brand_country.country == 'Япония':
                koef = data['JPY']
            elif cars[i].brand_country.country == 'Китай':
                koef = data['CNY']
            elif cars[i].brand_country.country == 'США':
                koef = data['USD']
            elif cars[i].brand_country.country == 'Европа':
                koef = data['EUR']
            elif cars[i].brand_country.country == 'Корея':
                koef = data['KRW']
            cars[i].price = int(koef * cars[i].price)

        for i in range(len(pop_cars)):
            if pop_cars[i].brand_country.country == 'Япония':
                koef = data['JPY']
            elif pop_cars[i].brand_country.country == 'Китай':
                koef = data['CNY']
            elif pop_cars[i].brand_country.country == 'США':
                koef = data['USD']
            elif pop_cars[i].brand_country.country == 'Европа':
                koef = data['EUR']
            elif pop_cars[i].brand_country.country == 'Корея':
                koef = data['KRW']
            pop_cars[i].price = int(koef * pop_cars[i].price)


    brands = Brand.objects.order_by('brand').filter(id__in=Car.objects.values('brand_country').distinct().values_list('brand_country'))
    drives = Car.objects.values('drive').distinct().order_by('drive')
    if not brand:
        models = Car.objects.values('model').distinct().order_by('model')
    else:
        models = Car.objects.values('model').distinct().order_by('model').filter(brand_country=brand)
    volumes = Car.objects.values('engine_volume').distinct().order_by('engine_volume')
    transmissions = Car.objects.values('transmission').distinct().order_by('transmission')
    colors = Car.objects.values('color').distinct().order_by('color')
    mileages = Car.objects.values('mileage').distinct().order_by('mileage')
    years = Car.objects.values('year').distinct().order_by('year')

    count_el = 12
    paginator = Paginator(cars, per_page=count_el)
    page_number = request.GET.get('page')
    try:
        page_obj = paginator.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = paginator.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = paginator.page(paginator.num_pages)
    cars = cars[count_el * (page_obj.number - 1):count_el * page_obj.number]
    return render(request, 'main/auto.html', {'cars': cars, 'page_obj': page_obj, 'pop_cars': pop_cars, 'brands': brands, 'drives': drives, 'models': models, 'transmissions': transmissions, 'colors': colors, 'years': years, 'volumes': volumes, 'mileages': mileages})

def car(request, id):
    car = Car.objects.get(id=id)
    if car.power_volume:
        power_volume = car.power_volume
    else:
        power_volume = "Нет данных о"
    if car.images != '':
        images = car.images.split('\n')
    else:
        images = []

    EURO_RATE = 100
    def calculate_customs_fee(car_price, engine_volume, car_age, EURO_RATE):
    # Пошлина
        if car_age <= 3:
            if car_price <= 8500 * EURO_RATE:
                customs_duty = max(0.54 * car_price, engine_volume * 2.5)
            elif car_price <= 16700 * EURO_RATE:
                customs_duty = max(0.48 * car_price, engine_volume * 3.5)
            elif car_price <= 42300 * EURO_RATE:
                customs_duty = max(0.48 * car_price, engine_volume * 5.5)
            elif car_price <= 84500 * EURO_RATE:
                customs_duty = max(0.48 * car_price, engine_volume * 7.5)
            elif car_price <= 169000 * EURO_RATE:
                customs_duty = max(0.48 * car_price, engine_volume * 15)
            else:
                customs_duty = max(0.48 * car_price, engine_volume * 20)
        elif car_age <= 5:
            if engine_volume <= 1000:
                customs_duty = engine_volume * 1.5 * EURO_RATE
            elif 1000 < engine_volume <= 1500:
                customs_duty = engine_volume * 1.7 * EURO_RATE
            elif 1500 < engine_volume <= 1800:
                customs_duty = engine_volume * 2.5 * EURO_RATE
            elif 1800 < engine_volume <= 2300:
                customs_duty = engine_volume * 2.7 * EURO_RATE
            elif 2300 < engine_volume <= 3000:
                customs_duty = engine_volume * 3 * EURO_RATE
            else:  # engine_volume > 3000
                customs_duty = engine_volume * 3.6 * EURO_RATE
        elif car_age >5:
            if engine_volume <= 1000:
                customs_duty = engine_volume * 3 * EURO_RATE
            elif 1000 < engine_volume <= 1500:
                customs_duty = engine_volume * 3.2 * EURO_RATE
            elif 1500 < engine_volume <= 1800:
                customs_duty = engine_volume * 3.5 * EURO_RATE
            elif 1800 < engine_volume <= 2300:
                customs_duty = engine_volume * 4.8 * EURO_RATE
            elif 2300 < engine_volume <= 3000:
                customs_duty = engine_volume * 5 * EURO_RATE
            else:  # engine_volume > 3000
                customs_duty = engine_volume * 5.7 * EURO_RATE
        # Утилизационный сбор
        if car_age <= 3:
            utilization_fee = 20000 * 0.17  # Базовый сбор для авто до 3 лет
        else:
            utilization_fee = 200000 * 0.26  # Для авто старше 3 лет
        # таможня
        if car_price <= 200000:
            tax = 775
        elif car_price <= 450000:
            tax = 1550
        elif car_price <= 1200000:
            tax = 3100
        elif car_price <= 2700000:
            tax = 8530
        elif car_price <= 4200000:
            tax = 12000
        elif car_price <= 5500000:
            tax = 15500
        elif car_price <= 7000000:
            tax = 20000
        elif car_price <= 8000000:
            tax = 23000
        elif car_price <= 9000000:
            tax = 25000
        elif car_price <= 10000000:
            tax = 27000
        elif car_price > 10000000:
            tax = 30000
        # Общая сумма
        total_customs_fee = customs_duty + utilization_fee + car_price + tax
        return {
            "Таможенная пошлина": round(customs_duty, 2),
            "Утилизационный сбор": round(utilization_fee,2),
            "НДС": round(tax, 2),
            "Итоговая сумма": round(total_customs_fee, 2)
        }
    
    eur = 100

    koef = 1
    with open(os.path.dirname(__file__) + '/modules/bank_course.json', 'r') as file:
        data = json.load(file)
        if car.brand_country.country == 'Япония':
            koef = data['JPY']
        elif car.brand_country.country == 'Китай':
            koef = data['CNY']
        elif car.brand_country.country == 'США':
            koef = data['USD']
        elif car.brand_country.country == 'Европа':
            koef = data['EUR']
        elif car.brand_country.country == 'Корея':
            koef = data['KRW']
        eur = data['EUR']


    if car.engine_volume != None:
        engine_volume = float(car.engine_volume)
    else:
        engine_volume = 2
    tax = calculate_customs_fee(car.price * koef, engine_volume, datetime.now().year - car.year, eur)
    return render(request, 'main/car.html', {'car': car, 'engine_volume': round(int(car.engine_volume) / 1000, 1), 'power_volume': power_volume, 'images': images, 'tax': tax, 'price': int(car.price * koef)})

def telegram(request):
    return redirect('https://t.me/TaiwanIsPartOfChina')

def whatapp(request):
    return redirect('https://contract.gosuslugi.ru/')

def vk(request):
    return redirect('https://contract.gosuslugi.ru/')

def instagram(request):
    return redirect('https://contract.gosuslugi.ru/')

def submit_form(request):
    name = request.GET.get('name')
    number = request.GET.get('number')
    text = request.GET.get('text')
    Request.objects.create(name=name, number=number, text=text)
    return redirect('/')