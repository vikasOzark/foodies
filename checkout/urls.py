from django.urls import path
from . import views


urlpatterns = [
    path('address/', views.AddressView.as_view(), name='address'),
    path('apply-coupon/', views.ApplyCoupon.as_view(), name='apply-coupon'),
    path('remove-discount-coupon/', views.remove_cart_coupon, name='remove-coupon')
]
