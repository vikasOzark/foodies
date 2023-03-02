from django.urls import path
from . import views  

urlpatterns = [
    path('', views.DashbordViews.as_view(), name='dashboard'),
    path('detail/<int:pk>/', views.OrderDetail.as_view(), name='detail'),
    path('kitchen/', views.KitchenView.as_view(), name='kitchen'),
    path('location_order/<str:location>/', views.LocationOrder.as_view(), name='location-order'),
    path('mark-deliver/<int:pk>/', views.mark_complete, name='mark_complete'),
    path('mark-cancel/<int:pk>/', views.mark_cancel, name='mark_cancel'),
]
