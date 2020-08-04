from django.contrib import admin
from .models import Item, Slider, Ad, Brand, OrderItem, Order
# Register your models here.
admin.site.register(Item)
admin.site.register(Slider)
admin.site.register(Ad)
admin.site.register(Brand)
admin.site.register(OrderItem)
admin.site.register(Order)