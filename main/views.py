from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import Car

# Create your views here.
def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')

def promo(request):
    return render(request, 'main/promo.html')

def contacts(request):
    return render(request, 'main/contacts.html')

def auto(request):
    cars = Car.objects.all()
    return render(request, 'main/auto.html', {'cars': cars})

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