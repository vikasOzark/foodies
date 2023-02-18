from django.contrib import admin
from . import models


@admin.register(models.OrderModel)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'order_id',
        'user',
        'cart',
        'address',
        'payment_status',
        'payment_id',
        'payment_mathod',
        'payment_partner',
    ]

    search_fields = ('order_id',)



admin.site.register(models.UserDetail)