from django.urls import path
from . import views


urlpatterns = [
    path('add-to-dabba', views.AddToCart.as_view(), name='Add_to_dabba'),
    path('', views.CartView.as_view(), name='my_cart'),
    path('buynow/<int:pk>/', views.BuyNowView.as_view(), name='buy_now'),
    path('update-cart/', views.cart_count_update, name='update-cart'),
    path('time-slot-update/', views.update_time_slot, name='time-slot-update'),
    path('update/', views.update_cart_quantity, name='update-qty'),
    path('delete_item/', views.delete_item, name='delete_item'),
]
