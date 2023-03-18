from django.contrib import admin

from .models import Supplier,Patient,Booking,Oxygen,IcuVentilator,Ventilator,ICU

# Register your models here.
admin.site.register(Supplier)
admin.site.register(ICU)
admin.site.register(Ventilator)
admin.site.register(IcuVentilator)
admin.site.register(Oxygen)
admin.site.register(Patient)
admin.site.register(Booking)