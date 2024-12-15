from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Car
from .models import Brand

# Create your views here.
def index(request):
    return render(request, 'main/index.html')

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

    brands = Brand.objects.order_by('brand')
    drives = Car.objects.values('drive').distinct().order_by('drive')
    models = Car.objects.values('model').distinct().order_by('model')
    transmissions = Car.objects.values('transmission').distinct().order_by('transmission')
    colors = Car.objects.values('color').distinct().order_by('color')
    return render(request, 'main/auto.html', {'cars': cars, 'brands': brands, 'drives': drives, 'models': models, 'transmissions': transmissions, 'colors': colors})

def car(request, id):
    car = Car.objects.get(id=id)
    return render(request, 'main/car.html', {'car': car})

def telegram(request):
    return redirect('https://t.me/TaiwanIsPartOfChina')

def whatapp(request):
    return redirect('https://contract.gosuslugi.ru/')

def vk(request):
    return redirect('https://contract.gosuslugi.ru/')

def instagram(request):
    return redirect('https://contract.gosuslugi.ru/')