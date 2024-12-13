from django.db import models

# Create your models here.
class Auto():
    id = models.PositiveIntegerField()
    model = models.CharField('Модель', max_length=50)
    year = models.PositiveIntegerField()
    miliege = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    power_volume = models.CharField('Модель', max_length=5)
    transmission = models.CharField(max_length=50)
    engine_volume = models.CharField(max_length=50)
    drive = models.CharField(max_length=50)
    color = models.CharField(max_length=50)

    def __str__(self):
        return self.model