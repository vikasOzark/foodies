from django.contrib import admin
from django.urls import path, include
from allauth import urls
from .sitemap import FoodSiteMap
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView 


sitemaps = {
    'food' : FoodSiteMap()
}

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
     name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', include('robots.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('',include('tiffine_site.urls')),
    path('cart/',include('cart.urls')),
    path('payment/',include('payment.urls')),
    path('order/',include('order.urls')),
    path('checkout/',include('checkout.urls')),
    path('superadmin/', include('dashboard.urls')),
    
]

handler404 = 'tiffine_site.views.handler404'
handler500 = 'tiffine_site.views.handler500'
