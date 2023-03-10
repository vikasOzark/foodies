from django.contrib import admin
from .models import MainDishModel, AddToFevorate, CommentAndRating, AddressModel, OrderDetails, Cart, Items, DeliveryCharges, Coupon, CustomersFavorite, PeopleFavorite

# Register your models here.


@admin.register(MainDishModel)
class Dishes(admin.ModelAdmin):
    list_display = ['id', 'name', 'deatil', 'price',
                    'discounted', 'image', 'ingredients', 'type_of', 'availablity']


@admin.register(AddToFevorate)
class Fvorite(admin.ModelAdmin):
    list_display = ['id', 'user', 'dish_name']


@admin.register(CommentAndRating)
class Ratings(admin.ModelAdmin):
    list_display = ['id', 'user', 'dish', 'comment', 'rating', 'timestamp']


@admin.register(AddressModel)
class UserAddress(admin.ModelAdmin):
    list_display = ['id', 'user', 'street',
                    'locality', 'landmark', 'city', 'phone', 'pincode']


@admin.register(OrderDetails)
class OrderDetail(admin.ModelAdmin):
    list_display = ['id', 'user', 'order_id', 'item_1', 'qyt_1',
                    'item_2', 'qyt_2', 'item_3', 'qyt_3', 'item_4', 'qyt_4', 'item_5', 'qyt_5',
                    'date_time', 'amount', 'payment_id', 'upi_transaction_id', 'vpa', 'card_id',
                    'bank', 'method', 'wallet']


@admin.register(Cart)
class CartDetails(admin.ModelAdmin):
    list_display = ['id', 'user']

@admin.register(Items)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart', 'food', 'quantity', 'unit_price', 'created'] 

@admin.register(DeliveryCharges)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['amount', 'is_active'] 


    
@admin.register(Coupon)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['coupon','type_of','value','validity','created','mode','active',] 

@admin.register(PeopleFavorite)
class PeopleFavoriteAdmin(admin.ModelAdmin):
    list_display = ['location'] 
