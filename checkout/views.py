from django.shortcuts import render, redirect
from django.views import generic
from tiffine_site.models import Coupon, Cart, AddressModel
from django.forms.models import model_to_dict
from django.http import JsonResponse
from order.views import  DashboardView
from checkout.models import BannersModel


class AddressView(generic.View):
    def get(self, request):
        template = 'address.html'
        context = self.get_context_data()
        return render(self.request, template, context=context)

    def post(self, *args, **kwargs):
        kwargs['checkout_address'] = True
        is_save = DashboardView().post(self.request, *args, **kwargs)
        if is_save:
            return redirect('payment')

    def get_queryset(self):
        super().get_queryset()
        return AddressModel.objects.filter(user=self.request.user).latest()
    
    def get_context_data(self, **kwargs):
        context = {}
        address = AddressModel.objects.filter(user=self.request.user)
        if len(address) == 1:
            context["address"] = address.first()
            context['form'] = model_to_dict(address.first())
        
        context['marketing'] = BannersModel.objects.filter(banner_type="ADDRESS_IMG").first()
        context['marketing_coupon'] = BannersModel.objects.filter(banner_type="ADDRESS-COUPON").first()
        
        return context

# def address_edit(request, pk):
#     template = 'address.html'
#     queryset = AddressModel.objects.filter(user=request.user, pk=pk).first()
#     return render(request, template, {})


# Create your views here.
class ApplyCoupon(generic.View):
    def post(self, *args, **kwargs):
        coupon_code = self.request.POST.get('coupon_code')
        cart_pk = self.request.POST.get('cart_pk')

        if self.request.user.is_authenticated:
            coupon_obj = Coupon.objects.filter(coupon=coupon_code).first()
            cart_obj = Cart.objects.filter(pk = cart_pk, user=self.request.user).first()

            if coupon_obj is None:
                return JsonResponse({'status':404, 'message' : 'Not a valid code please check !'})

            if cart_obj.coupon_applied == 1:
                return JsonResponse({'status': 301, 'message': 'Already used !'})

            if coupon_obj.check_coupon_validity():
                amount = 0
                type_of = coupon_obj.type_of
                if type_of == 'VALUE':
                    amount = coupon_obj.value
                else:
                    cart_amount = int(cart_obj.get_delivery_amount())
                    value = int(coupon_obj.value)
                    discount_amount = (cart_amount * value) / 100
                    amount = cart_amount - discount_amount
                    
                cart_obj.coupond_amount = amount
                cart_obj.coupon_used = coupon_code
                cart_obj.coupon_applied = 1
                cart_obj.save()

                return JsonResponse({'status':200, 'message': 'Applied !'})
            return JsonResponse({'status':404, 'message': 'Oops , Coupon is expired !'})
            
def remove_cart_coupon(request):
    data = request.POST
    cart_obj = Cart.objects.filter(pk=data.get('cart_pk')).first()
    cart_obj.coupond_amount = 0
    cart_obj.coupon_used = ''
    cart_obj.coupon_applied = 0
    cart_obj.save()
    return JsonResponse({'status':200})
