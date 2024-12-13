from django.db import models

# Create your models here.
class Brand(models.Model):
    country = models.CharField('Страна', max_length=150)
    brand = models.CharField('Модель', max_length=150)

    def __str__(self):
        return f'{self.brand} | {self.country}'

class Car(models.Model):
    model = models.CharField('Бренд', max_length=50)
    year = models.IntegerField('Год')
    mileage = models.IntegerField('Пробег')
    price = models.IntegerField('Цена')
    transmission = models.CharField('Трасмиссия', max_length=50)
    engine_volume = models.CharField('Мощность двигателя', max_length=50)
    drive = models.CharField('Привод', max_length=50)
    color = models.CharField('Цвет', max_length=50)
    power_volume = models.CharField('Мощность', max_length=5)
    brand_country = models.ForeignKey(Brand, on_delete=models.DO_NOTHING, blank=True, null=True)

    def __str__(self):
        return f'{self.brand_country.brand} {self.model}'
