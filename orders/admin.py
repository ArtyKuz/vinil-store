from django.contrib import admin

from orders.models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'address', 'total_price', 'created', 'status')
    # filter_horizontal = ('order_albums',)