from django.shortcuts import render
from tiffine_site import models as t_model
from django.views import generic
from . import serializers
from cart.views import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib.auth.models import User
from itertools import chain
from dataclasses import dataclass
from django.db.models import QuerySet
from . import models
from typing import Any, Dict
from order.models import OrderModel, UserDetail
from django.contrib import messages



class DashboardView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        DASHBOARD = kwargs.get('detail_type')
        if DASHBOARD == 'address':
            address = t_model.AddressModel.objects.filter(user=self.request.user)
            context['addresses'] = address
        
        if DASHBOARD == 'orders':
            my_orders = OrderModel.objects.filter(user=self.request.user).select_related('user', 'cart')
            context['my_orders'] = my_orders
            
        context['user_data'] = UserDetail.objects.filter(user=self.request.user).first()
        if DASHBOARD  is None:
            DASHBOARD = 'basic'
        context["detail_type"] = DASHBOARD
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST
        data._mutable = True
        data['user'] = request.user.id

        for field in data:
            if data[field] == None: 
                data[field] == ''
        data._mutable = False

        if data.get('form_type') == 'address':
            qs = t_model.AddressModel.objects.filter(user=request.user).first()
            serializer = serializers.AddressSerializers(instance=qs ,data=data)
            if serializer.is_valid():
                serializer.save()
            else:
                print(serializer.errors)

        if data.get('form_type') == 'detail':
            detail = UserDetail.objects.filter(
                user=self.request.user)

            if len(detail ) != 0:
                detail.update(
                phone=data.get('phone'),
                altenate_number=data.get('alternate_phone'))
            else:
                detail = UserDetail.objects.create(
                user=self.request.user,
                phone=data.get('phone'),
                altenate_number=data.get('alternate_phone'))


        if kwargs.get('checkout_address') is not None:
            return True
        return self.get(request)


    def get_order(self, filter:str=None) -> QuerySet:
        orders = OrderModel.objects.filter(user=self.request.user)
        if not filter:
            return orders.filter() 
        return 
    

def delete_address(request):
    id = request.POST.get('pk')
    t_model.AddressModel.objects.filter(pk=id).first().delete()
    return JsonResponse({'status':200})

@dataclass
class OrderHandler(generic.View):
    cart_object : QuerySet
    
    def create_order(self,address, user, time_slot, data_dict:dict) -> int:
        """this function takes required data to save data to the DB"""

        try:
            order_object = models.OrderModel.objects.create(
                user = user, 
                cart = self.cart_object,
                address = address,
                payment_status = data_dict.get('payment_status'), 
                payment_id = data_dict.get('payment_id'), 
                payment_response = data_dict.get('payment_response'), 
                payment_mathod = 'ONLINE', 
                payment_signature = data_dict.get('payment_signature'), 
                payment_partner = data_dict.get('payment_partner'), 
                time_slot = time_slot,
                payment_type = data_dict.get('payment_mathod')
            )
            return order_object.order_id
        except:
            return False

class CODPaymentHandler(generic.View):
    def post(self, *args, **kwargs):
        cart = t_model.Cart.objects.filter(
            cart_id=self.request.session.get('cart')).first()

        order_object = models.OrderModel.objects.create(
            user = self.request.user, 
            cart = cart,
            payment_status = 'PENDING',
            address = t_model.AddressModel.objects.filter(user=self.request.user).first(),
            time_slot = self.request.session.get('time-slot'),
            payment_mathod = 'COD'
         )
        cart.is_complete = True
        cart.save()
        del self.request.session['cart']
        del self.request.session['time-slot']
        return JsonResponse({'status':200, 'order_id':order_object.order_id})

class ThankYouSuccess(generic.View):
    def get(self, *args, **kwargs):
        if not kwargs.get('order_id'):
            return render('dashboard')
        
        template_name = 'success.html'
        return render(self.request, template_name, context=self.get_context_data(**kwargs))

    def get_queryset(self, *args, **kwargs):
        return OrderModel.objects.get(order_id=kwargs.get('order_id'))
    
    def get_context_data(self, **kwargs):
        context = {}
        context["order"] = self.get_queryset(**kwargs)
        return context
    

def faild_order(request, id=None):
    template='faild.html'
    context={'id':id}
    return render(request, template, context)


def user_detail_save(request:dict) -> JsonResponse:
    data = request.POST
    detail = models.UserDetail.objects.create(
        phone=data.get('phone'),
        altenate_number=data.get('alternate')
    )
    
    return JsonResponse({'status':200})