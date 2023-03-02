from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView


urlpatterns = [
    path('not', IndexView.as_view(), name='index'),
    path('', MenuView.as_view(), name='menu'),
    path('menu/<slug:slug>', MenuView.as_view(), name='menu'),
    path('<slug:slug>', FoodDeatail.as_view(), name='deatail-view'),
    path('payment-checkout/',
         PaymentCheckout.as_view(), name='payment-checkout'),
    path('payment-checkout/<int:pk>',
         PaymentCheckout.as_view(), name='payment-checkout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login, name='login'),
    path('logout_user/', logout_user, name='logout_user'),
    path('add-favorite/', add_favorite, name='add-favorite'),
    path('user-profile/', user_profile, name='user-profile'),
    path('change-pass', change_passwd, name='change-pass'),
    path('filter_menu/', filter_menu, name='filter_menu'),
    path('user-profile/sav_address/', sav_address, name='sav_address'),
    path('delete-addr/', delete_address, name='delete-addr'),
    path('edit-addr', edit_address, name='edit-addr'),
    path('raring/', ratings, name='rating'),
    path('add-to-dabba', AddToDabba, name='Add_to_dabba'),
    path('adding_quantity/', adding_quantity, name='adding_quantity'),
    path('total_amount/', total_amount, name='total_amount'),
    path('favorite-temp/', favorite_temp, name='favorite-temp'),
    path('data/', returndata ),
    path('privacy-policy/', TemplateView.as_view(template_name="privacypolicy.html"), name='privacy-policy'),
    path('term-condition/', TemplateView.as_view(template_name="term_condition.html"), name='term-condition'),
    path('contact-us/', TemplateView.as_view(template_name="contactus.html"), name='contact-us'),



    # path('buy-now/', BuyNowView.as_view(), name='buy_now')

    # these lins are for password reset with email link
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='password_reset_form.html'
    ), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
         template_name='password_reset_done.html'
         ), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        #     template_name='password_reset_confirm.html'
    ),
        name='password_reset_confirm'),

    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(
         template_name='password_reset_complete.html'
         ),
         name='password_reset_complete'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL,
#                           document_root=settings.MEDIA_ROOT)
