from django.urls import path
from . import views


urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashbord'),
    path('dashboard-type/<str:detail_type>/', views.DashboardView.as_view(), name='dashbord-type'),
    path('delete-address/', views.delete_address, name='address-delete'),
    path('thank-you/<str:order_id>/', views.ThankYouSuccess.as_view(), name='thank-you'),
    path('faild/<str:id>/', views.faild_order, name='faild'),
    path('cod-order/', views.CODPaymentHandler.as_view(), name='cod-order'),

]
