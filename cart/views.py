from django.shortcuts import render, redirect
from tiffine_site.models import MainDishModel, Cart, Items
from django.views import generic
from django.db.models import Q
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from checkout.models import BannersModel


# Create your views here.

class AddToCart(generic.View):
    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return JsonResponse({'status':401})
        
        id = self.request.GET.get('dish_id')
        food = MainDishModel.objects.get(pk=id)

        if self.request.session.get('cart') is None:
            create_cart(self.request)

        cart_id = self.request.session.get('cart')
        item = Items.objects.filter(cart=cart_id , food=food).exists()

        if not item:
            Items.objects.create(cart = cart_id, food=food)
            return JsonResponse({'status': 200})
        else:
            Items.objects.get(Q(cart = cart_id) & Q(food=food)).delete()
            return JsonResponse({'status':204})

    def post(self, *args, **kwargs):
        return JsonResponse({'status' : 200})

def create_cart(request=None):
    cart = Cart.objects.create(
        user = request.user)
    request.session['cart'] = cart.cart_id
    return cart.cart_id


class BuyNowView(LoginRequiredMixin, generic.View):
    template = 'payment_checkout.html'
    def get(self, *args, **kwargs):
        id = kwargs.get('pk')

        cart_id = self.request.session.get('cart')
        if cart_id is None:
            create_cart(self.request)

        food = MainDishModel.objects.get(pk=id)
        item_ins = Items.objects.filter(cart=cart_id, food=food).exists()
        if item_ins:
            item_ins = Items.objects.get(cart=cart_id, food=food)
            item_ins.quantity += 1
            item_ins.save()
        else:
            cart_id = self.request.session.get('cart')
            Items.objects.create(cart=cart_id, food=food)
        return redirect('my_cart')


class CartView(LoginRequiredMixin, generic.View):
    def get(self, *args, **kwargs):
        template_name = 'payment_checkout.html'
        cart_id = self.request.session.get('cart')
        if cart_id is None:
            return redirect('menu')
        return render(self.request, template_name, self.get_context_data(cart_id))

    def get_context_data(self, cart_id, **kwargs):
        context = {}
        cart = Cart.objects.filter(Q(user=self.request.user) & Q(cart_id=cart_id)).latest()
        cart_item = cart.get_cart_items()
        context['items'] = cart_item
        context['cart'] = cart
        context['marketing'] = BannersModel.objects.filter(banner_type='CART_IMG').first()
        return context

def delete_item(request):
    pk = request.GET.get('item_obj')
    cart_id = request.session.get('cart')
    Items.objects.get(Q(pk=pk) & Q(cart=cart_id)).delete()

    cart_obj = Cart.objects.filter(Q(user=request.user) & Q(cart_id=cart_id)).latest()
    if len(cart_obj.get_cart_items()) == 0 and cart_obj.coupon_used != '':
        cart_obj.coupon_applied = 0
        cart_obj.coupond_amount = 0
        cart_obj.coupon_used = ''
        cart_obj.save()
    
    return JsonResponse({'status' : 200})


def cart_count_update(request):
    if request.user.is_authenticated:
        cart_id = request.session.get('cart')
        if cart_id is not None:
            count = Cart.objects.filter(Q(user=request.user) & Q(cart_id=cart_id)).latest().get_cart_items().count()
        else: count = 0
    else:
        count = 0
    return JsonResponse({'count':count}) 


def update_time_slot(request):
    request.session['time-slot'] = request.GET.get('time_slot').upper()
    return JsonResponse({'status' : 200})

def update_cart_quantity(request) -> JsonResponse:
    queyr_data = request.GET
    data = {}

    cart_id = request.session.get('cart')
    cart_object = Cart.objects.filter(Q(user=request.user) & Q(cart_id=cart_id)).latest()
    filter_itme = cart_object.get_cart_items().get(pk=queyr_data.get('item_obj'))
    
    if queyr_data.get('action') == 'plus':
        filter_itme.quantity += 1
    else:
        filter_itme.quantity -= 1
    filter_itme.save()

    cart_object = Cart.objects.filter(Q(user=request.user) & Q(cart_id=cart_id)).latest()
    data['get_cart_price'] = cart_object.get_cart_price()
    data['delivery_charge'] = cart_object.delivery_charge()
    data['coupond_amount'] = cart_object.coupond_amount
    data['get_delivery_amount'] = cart_object.get_delivery_amount()
    data['quantity'] = cart_object.get_cart_items().get(pk=queyr_data.get('item_obj')).quantity

    
    return JsonResponse(data)