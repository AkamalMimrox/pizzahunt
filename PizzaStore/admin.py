from django.contrib import admin
from .models import CategoriesMaster, ProductMaster, about, Social, PaymentStatus

# Register your models here.

admin.site.register([CategoriesMaster,ProductMaster,about,Social,PaymentStatus])
