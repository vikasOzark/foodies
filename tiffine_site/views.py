from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from .models import MainDishModel, AddToFevorate, AddressModel, CommentAndRating, Cart, OrderDetails, Items, CustomersFavorite
from django.db.models import Q
from django.core import serializers
from .forms import AddressForm
from django.views.decorators.csrf import csrf_exempt
import razorpay
from django.conf import settings
from .serializers import AddressSerializers
from django.forms.models import model_to_dict
import datetime
from django.db.models import Q

# from django.shortcuts import render_to_response
from django.template import RequestContext


# Create your views here.

# RAZOR_KEY_ID = 'rzp_test_HwKecOzHzISyXr'
# RAZOR_KEY_SECRET = 'bDcjVc789fO9Prz8kCDgm2yP'


class IndexView(View):
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, template_name='index.html', context=context)   

    def get_context_data(self, *args, **kwargs):
        context = {}
        context['customer_fav'] = self.customers_fav()
        context['customer_review'] = self.customer_review()
        return context

    def customers_fav(self, *args, **kwargs):
        return CustomersFavorite.objects.all()

    def customer_review(self, *args, **kwargs):
        return CommentAndRating.objects.filter(is_show=True)[:6]


class MenuView(View):
    def get(self, request, slug=None, *args, **kwargs):

        if request.user.is_authenticated:
            favorite = AddToFevorate.objects.filter(user=request.user)
            is_cart = Cart.objects.filter(user=request.user)

            if slug == 'veg':
                menu_model = MainDishModel.objects.filter(type_of='veg')
            elif slug == 'non_veg':
                menu_model = MainDishModel.objects.filter(type_of='non_veg')
            else:
                menu_model = MainDishModel.objects.all()

            template = 'menu.html'

            context = {
                'menu_model': menu_model,
                'fav': favorite,
                'is_cart': is_cart,
                'slug' : slug

            }
            return render(request, template_name=template, context=context)
        else:

            if slug == 'veg':
                menu_model = MainDishModel.objects.filter(type_of='veg')
            elif slug == 'non_veg':
                menu_model = MainDishModel.objects.filter(type_of='non_veg')
            elif slug == 'all':
                menu_model = MainDishModel.objects.all()
            else:
                menu_model = MainDishModel.objects.all()

            template = 'menu.html'

            context = {
                'menu_model': menu_model,
                'slug' : slug
            }
            return render(request, template_name=template, context=context)


class FoodDeatail(View):
    def get(self, request, *args, **kwargs):


        dish_obj = MainDishModel.objects.filter(slug=kwargs['slug']).first()
        rating_obj = CommentAndRating.objects.filter(dish=dish_obj)

        if request.user.is_authenticated:
            favorite = AddToFevorate.objects.filter(user=request.user)
            is_cart = '' #Cart.objects.filter(Q(user=request.user) & Q(item=dish_obj)).values_list('item__id', flat=True)
            is_cart = '' #Items.objects.filter(Q(user=request.user) & Q())
            is_c = '' #Cart.objects.filter(
                #
            is_favorite = AddToFevorate.objects.filter(
                Q(user=request.user) & Q(dish_name__slug=kwargs['slug'])).exists()

            context = {
                'fav': favorite,
                'is_favorite': is_favorite,
                'rating_obj': rating_obj,
                'is_cart': is_cart,
                'is_c': is_c,
                'dish_obj': dish_obj,
                'rating_obj': rating_obj,
            }

        context = {
            'dish_obj': dish_obj,
            'rating_obj': rating_obj,
        }
        template = 'deatail_view.html'
        return render(request, template_name=template, context=context)


razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


class PaymentCheckout(View):
    razorpay_client = razorpay.Client(
        auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

    def get(self, request, *args, **kwargs):
        if kwargs.get('pk') is not None:
            cart_instance = self.create_cart_item(*args, **kwargs)
        else:
            cart_instance = Cart.objects.get(Q(user=request.user) & Q(cart_id=kwargs.get('cart_id'))).get_cart_items()

        final_amount = 0
        for obj in cart_instance:
            qyt_ins = obj.quantity
            amount_ins = obj.item.discounted
            final_amount += amount_ins * qyt_ins

        currency = 'INR'
        amount = (final_amount + 50) * 100

        plus_delivery = final_amount + 50
        # Create a Razorpay Order
        razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                           currency=currency,
                                                           payment_capture='0'))

        # order id of newly created order.
        razorpay_order_id = razorpay_order['id']
        # callback_url = 'paymenthandler'
        template = 'payment_checkout.html'

        context = {
            'dish_instance': cart_instance,
            'razorpay_order_id': razorpay_order_id,
            'razorpay_merchant_key': 'rzp_test_CACIK9VunIicKe',
            'razorpay_amount': amount,
            'currency': currency,
            # 'callback_url': callback_url
            'final_amount': final_amount,
            'plus_delivery': plus_delivery,
        }
        return render(request, template_name=template, context=context)

    def create_cart_item(self, *args, **kwargs):
        food = MainDishModel.objects.get(pk=kwargs.get('pk'))
        item = Cart(
            user = self.request.user,
            item = food,
            quantity = 1,
        )
        item_obj = item.save()
        return item_obj





class RegisterView(View):
    def get(self, request):
        return render(request, template_name='register.html')

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if not all(request.POST.values()):
            messages.info(request, 'We are missing some fields.')
            return render(request, template_name='register.html')
    
        if password != password2:
            messages.info(request, "Your password din't match !")
            return render(request, template_name='register.html')

        user = User.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=email,
            password=password,
        )
        user.save()
        user.set_password(user.password)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request, f"{user.username}, You successfully registered !",
                                extra_tags='alert-success')
            return redirect("menu")


 


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        passwd = request.POST.get('password')

        user = authenticate(request, username=username, password=passwd)
        if user is not None:
            auth_login(request, user)
            return redirect('menu')
        else:
            messages.warning(request, "Username or password didn't match")
            return redirect('login')

    return render(request, template_name='login.html')


def logout_user(request):
    logout(request)
    return redirect('menu')


def add_favorite(request):
    if request.method == "GET":
        prod_id = request.GET.get('item_id')
        dish_obj = MainDishModel.objects.get(id=prod_id)

        is_favorite = AddToFevorate.objects.filter(
            Q(user=request.user) & Q(dish_name=dish_obj)).exists()
        if is_favorite == False:
            save_fav = AddToFevorate(user=request.user, dish_name=dish_obj)
            save_fav.save()
            return JsonResponse({'status': 'Save', 'data_coming': 'red'})
        else:
            favorite = AddToFevorate.objects.get(
                Q(user=request.user) and Q(dish_name=dish_obj))
            favorite.delete()
            return JsonResponse({'status': 'Deleted', 'data_coming': 'black'})


@login_required(login_url='login')
def user_profile(request):
    address = AddressModel.objects.filter(user=request.user)
    orders = OrderDetails.objects.filter(user=request.user)
    phones = AddressModel.objects.filter(user=request.user)
    try:
        phone = []
        for i in phones:
            phone.append(i.phone)
        context = {
            'address': address,
            'add_form': AddressForm,
            'orders': orders,
            'phone': phone[0]
        }
        template = 'profile.html'
        return render(request, template_name=template, context=context)

    except:
        phone = ['Please add number while adding address !']

        context = {
            'address': address,
            'add_form': AddressForm,
            'orders': orders,
            'phone': phone[0]
        }
        template = 'profile.html'
        return render(request, template_name=template, context=context)


def change_passwd(request):
    if request.method == "POST":

        password = request.POST.get('password')
        new_passwd = request.POST.get('new_passwd')
        new_passwd2 = request.POST.get('new_passwd2')

        if new_passwd == new_passwd2:
            user = authenticate(
                request, username=request.user, password=password)

            if user is not None:
                passwd = User.objects.get(username=request.user)
                passwd.set_password(new_passwd)
                passwd.save()
                logout(request)

                message = messages.info(
                    request, 'Congrats, You have successfully changed your password !')
                try:
                    return redirect('login')
                except:
                    return JsonResponse({'status': 'done'})
            else:
                message = messages.warning(
                    request, 'Your old password is wrong !', extra_tags='')
                return JsonResponse({'status': 'old passwor wrong'})
        else:
            message = messages.info(request, 'Password supposed to be same  !')
            return JsonResponse({'status': 'not matched'})


def filter_menu(request):
    if request.method == 'GET':
        type_of = request.GET.get('type_val')
        if type_of == 'non_veg':
            data = serializers.serialize(
                "json", MainDishModel.objects.filter(type_of=type_of), fields=(
                    'name', 'deatil', 'price', 'discounted', 'availablity', 'image', 'ingredients', 'type_of'))
            return JsonResponse({'status': 'working', 'datas': data})
        if type_of == 'veg':
            data = serializers.serialize(
                "json", MainDishModel.objects.filter(type_of=type_of), fields=(
                    'name', 'deatil', 'price', 'discounted', 'availablity', 'image', 'ingredients', 'type_of'))
            return JsonResponse({'status': 'working', 'datas': data})


def sav_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            street = request.POST['street']
            locality = request.POST['locality']
            landmark = request.POST['landmark']
            city = request.POST['city']
            phone = request.POST['phone']
            pincode = request.POST['pincode']
            id = request.POST.get('id')

            if id == '':
                address_obj = AddressModel(
                    user=request.user,
                    street=street,
                    locality=locality,
                    landmark=landmark,
                    city=city,
                    phone=phone,
                    pincode=pincode,
                )
            else:
                address_obj = AddressModel(
                    user=request.user,
                    id=id,
                    street=street,
                    locality=locality,
                    landmark=landmark,
                    city=city,
                    phone=phone,
                    pincode=pincode,
                )
            address_obj.save()

            data_obj = AddressModel.objects.values()
            data_obj = list(data_obj)

            messages.success(request, 'Address saved successfully  !', extra_tags='')
            return JsonResponse({'status': 'saved', 'data_obj': data_obj})
        else:
            messages.info(request, 'Address not saved !')
            return JsonResponse({'status': 'Wrong', 'data_obj': data_obj})


def delete_address(request):
    if request.method == "POST":
        id = request.POST.get('sid')
        addr_obj = AddressModel.objects.get(pk=id)
        addr_obj.delete()
        return JsonResponse({'status': '200'})
    else:
        return JsonResponse({'status': '420'})


def edit_address(request):
    if request.method == 'POST':
        id = request.POST.get('sid')
        addr_obj = AddressModel.objects.get(pk=id)
        addr_data = {
            'street': addr_obj.street,
            'landmark': addr_obj.landmark,
            'city': addr_obj.city,
            'locality': addr_obj.locality,
            'pincode': addr_obj.pincode,
            'phone': addr_obj.phone,
            'id': addr_obj.id
        }
        return JsonResponse(addr_data)


@login_required()
def ratings(request):
    if request.method == 'GET':
        comment = request.GET.get('comment')
        rating = request.GET.get('userRating')
        id = request.GET.get('id')
        dish_obj = MainDishModel.objects.get(pk=id)

        model_ins = CommentAndRating(
            user=request.user,
            dish=dish_obj,
            comment=comment,
            rating=rating
        )

        model_ins.save()
        model_obj = CommentAndRating.objects.values()
        model_obj = list(model_obj)
        return JsonResponse({'status': '200', 'objects': model_obj})


def AddToDabba(request):
    if request.method == 'GET':
        cart_id = request.session.get('cart_id')
        if cart_id is None:
            cart = Cart(
                user = request.user
            )
            cart_obj = cart.save()
            request.session['cart_id'] = cart_obj.cart_id
            return AddToDabba(request)
        
        id_ = request.GET.get('dish_id')
        item_obj = MainDishModel.objects.get(pk=id_)
        is_cart = Items(
            Q(user=request.user) & Q(food=item_obj) & Q(cart_id=cart_id)).exists()

        if is_cart:
            obj = Items.objects.get(Q(user=request.user) & Q(item=item_obj) & Q(cart=cart_id))
            obj.delete()
            return JsonResponse({'status': 'delete', 'is_cart': 'Add cart'})
        else:
            cart_instance = Items(
                user=request.user,
                food=item_obj,
                quantity=1,
            )

            cart_instance.save()

            return JsonResponse({'status': 'save', 'is_cart': 'Added'})

    if request.method == 'POST':
        id_ = request.POST.get('dish_id')
        try:
            get_obj = Cart.objects.get(Q(pk=id_) & Q(user=request.user))
            get_obj.delete()

            return JsonResponse({'status': 'delete'})
        except:
            return JsonResponse({'status': '400'})


def adding_quantity(request):
    if request.method == 'GET':
        item_id = request.GET.get('item_id')
        qty_val = request.GET.get('quantity')

        item_id = int(item_id)
        qty_val = int(qty_val)

        cart_obj = Cart.objects.get(
            id=item_id,
        )
        cart_obj.quantity = qty_val
        cart_obj.save()

        return JsonResponse({'status': 'Updated'})


def total_amount(request):
    if request.method == 'GET':

        cart = Cart.objects.filter(user=request.user)

        final_amount = 0
        for obj in cart:
            qyt_ins = obj.quantity
            amount_ins = obj.item.discounted
            final_amount += amount_ins * qyt_ins

        plus_delivery = final_amount + 50

        data = {
            'final_amount': final_amount,
            'plus_delivery': plus_delivery,
        }
    return JsonResponse(data)


def favorite_temp(request):
    favorite_obj = AddToFevorate.objects.filter(user=request.user)

    template = 'favorite_template.html'
    context = {
        'favorite_obj': favorite_obj,
    }

    return render(request, template_name=template, context=context)


def handler404(request, exception):
    context = {}
    response = render(request, "404.html", context=context)
    response.status_code = 404
    return response


def handler500(request):
    context = {}
    response = render(request, ".500.html", context=context)
    response.status_code = 500
    return response