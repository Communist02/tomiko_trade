from django.shortcuts import redirect, render
from .models import Car
from .models import Brand
from .models import Request
from django.db.models.lookups import GreaterThanOrEqual
from django.db.models.lookups import LessThanOrEqual
from django.db.models import F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def index(request):
    cars = Car.objects.all()[:10]
    id = 456242135
    id_clips =  [i for i in range(id, id+10)]
    return render(request, 'main/index.html', {'pop_cars': cars, 'clips': id_clips})

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
    print(page_obj.number)
    cars = cars[count_el * (page_obj.number - 1):count_el * page_obj.number]
    return render(request, 'main/auto.html', {'cars': cars, 'page_obj': page_obj, 'pop_cars': Car.objects.all()[:10], 'brands': brands, 'drives': drives, 'models': models, 'transmissions': transmissions, 'colors': colors, 'years': years, 'volumes': volumes, 'mileages': mileages})

def car(request, id):
    car = Car.objects.get(id=id)
    if car.power_volume:
        power_volume = car.power_volume
    else:
        power_volume = "Нет данных о"
    return render(request, 'main/car.html', {'car': car, 'engine_volume': round(int(car.engine_volume) / 1000, 1), 'power_volume': power_volume})

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