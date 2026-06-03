from django.contrib import admin

from .models import Booking, Cart, Category, MenuItem, Order, OrderItem

# register models
admin.site.register(MenuItem)
admin.site.register(Booking)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
