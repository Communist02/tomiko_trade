from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about_us', views.about_us, name='about_us'),
    path('promo', views.promo, name='promo'),
    path('contacts', views.contacts, name='contacts'),
    path('auto', views.auto, name='auto'),
    path('car/<id>', views.car, name='car'),
    path('telegram', views.telegram, name='telegram'),
    path('whatapp', views.whatapp, name='whatapp'),
    path('vk', views.vk, name='vk'),
    path('instagram', views.instagram, name='instagram')
]