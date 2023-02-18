from django.urls import path
from . import views

urlpatterns = [
    path('', views.PaymentView.as_view(), name='payment'),
    path('payment-callback/', views.payment_response_handler, name='payment-callback'),
]
