from django.contrib import admin
from django.urls import path, include
from allauth import urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('',include('tiffine_site.urls')),
    path('cart/',include('cart.urls')),
    path('payment/',include('payment.urls')),
    path('order/',include('order.urls')),
    path('checkout/',include('checkout.urls')),
]

handler404 = 'tiffine_site.views.handler404'
handler500 = 'tiffine_site.views.handler500'
