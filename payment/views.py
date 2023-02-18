from django.shortcuts import render, redirect
from django.views import generic
from tiffine_site.models import Cart, AddressModel
from django.db.models import Q
import razorpay
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from order import views as order_view
from checkout.models import BannersModel


RAZORPAY_CLIENT = razorpay.Client(
            auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


# Create your views here.
class PaymentView(generic.View):
    def get(self, *args, **kwargs):
        if not self.request.session.get('cart'):
            return redirect('menu')
        
        template='payments.html'
        cart = self.request.session.get('cart')
        cart_obj = Cart.objects.filter(Q(cart_id=cart) & Q(user=self.request.user)).first()

        # if amount is less that min amount redirect to the menu page
        if cart_obj.get_cart_price() < 50:
            return redirect('menu')

        context = {}
        context['cart_obj'] = cart_obj
        context['razor_pay'] = CreatePaymentHandler().payment_create(
            amount=cart_obj.get_delivery_amount(), 
            callback=f'http://127.0.0.1:8000/payment/payment-callback/?id={cart}', 
            cart_id=cart)
        # context['marketing'] = BannersModel.objects
        return render(self.request, template, context)

@csrf_exempt
def payment_response_handler(request):
    payment_handler = CreatePaymentHandler()
    check_out_payment = payment_handler.filter_payment_response(
                            request
                        )
    is_payment_success = payment_handler.verify_payment(
                            check_out_payment,
                            120,
                        )
    if is_payment_success[0]:
        cart = Cart.objects.filter(cart_id=request.session.get('cart')).first()
        address = AddressModel.objects.filter(user=request.user).first()
        response = payment_handler.capture_payment(is_payment_success[1].get('razorpay_payment_id'))

        is_save = order_view.OrderHandler(cart).create_order(
            user=request.user,
            address=address,
            time_slot = request.session.get('time-slot'),
            data_dict={
                'payment_status' : 'CONFIRM',
                'payment_id' : is_payment_success[1].get('razorpay_payment_id'),
                'payment_response' : response,
                'payment_mathod' : response.get('method'),
                'payment_signature' : is_payment_success[1].get('razorpay_signature'),
                'payment_partner' : 'RAZORPAY',
            },
        )
        
        if is_save:
            cart.is_complete = True
            cart.save()
            del request.session['cart']
            del request.session['time-slot']
            return redirect('thank-you', order_id=is_save)
            
        else:
            result = payment_handler.check_faild_payment(is_payment_success[1].get('razorpay_order_id'))
            if not result:
                return redirect('faild', )
            else:
                return redirect('thank-you', order_id=is_save)

        


class CreatePaymentHandler:
    def payment_create(*args, **kwargs):
        razorpay_order = RAZORPAY_CLIENT.order.create({
            'amount': kwargs.get('amount') * 100,
            'currency':'INR',
            'notes': {'cart':kwargs.get('cart_id')},
        })

        # order id of newly created order.
        return {
            'razorpay_order_id': razorpay_order['id'],
            'razorpay_merchant_key': settings.RAZOR_PAY_SECRET,
            'razorpay_amount': (kwargs.get('amount') * 100),
            'callback_url': kwargs.get('callback')
            }


    @staticmethod
    def filter_payment_response(request) -> dict:
        """this function filter the POST data"""
        # only accept POST request.
        # get the required parameters from post request.
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')
        notes = request.POST.get('notes')

        return {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature,
            'notes' : notes,
        }

    def verify_payment(self, response:dict, amount:int, cart_id:str=None) -> None:
        """this function returns result and response dict
        Args:
            response (dict): response from the request.POST
            amount (int): Cart amount
            cart_id:
        Returns:
            set: (result:True, response:dict)
        """ 
        result = RAZORPAY_CLIENT.utility.verify_payment_signature(
            response)

        return result, response


    def capture_payment(self, payment:str) -> dict:
        """retrive the payment response form the razorpay server"""
        reutrn_res = RAZORPAY_CLIENT.payment.fetch(payment)
        return reutrn_res


    def check_faild_payment(self, order_id:str) -> bool:
        check_payment = RAZORPAY_CLIENT.order.payments(order_id)
        if check_payment.get('items')[0].get('status') != 'captured':
            return False
        else:
            return True


