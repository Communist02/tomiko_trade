from django.contrib import admin
from .models import Brand
from .models import Car
from .models import Request

# Register your models here.
admin.site.register(Brand)
admin.site.register(Car)
admin.site.register(Request)