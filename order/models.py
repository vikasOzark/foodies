from django.db import models
from tiffine_site import models as tiffines
from django.contrib.auth.models import User
import random
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from datetime import datetime, timedelta


class OrderManager(models.Manager):
    def get_queryset(self):
        return super(OrderManager, self).get_queryset().filter(order_status='DELIVERD')

class OrderModel(models.Model):
    STATUS = (
        ('PENDING', 'PENDING'),
        ('CONFIRM' , 'CONFIRM'),
        ('CANCEL', 'CANCEL'),
        ('FAILD', 'FAILD'),
    )

    DELIVERY_STATUS = (
        ('PENDING', 'PENDING'),
        ('DELIVERD', 'DELIVERD'),
        ('CANCEL', 'CANCEL')
    )

    METHODS = (
        ('COD', 'COD'),
        ('ONLINE', 'ONLINE'),
    )

    PAYMENT_PARTNER = (
        ('RAZORPAY', 'RAZORPAY'),
    )

    TIMESLOT = (
        ('BREAKFAST', 'BREAKFAST'),
        ('LUNCH', 'LUNCH'),
        ('DINNER' , 'DINNER')
    )

    order_id = models.CharField(max_length=100, unique=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(tiffines.Cart, on_delete=models.CASCADE)
    address = models.ForeignKey(tiffines.AddressModel, on_delete=models.DO_NOTHING)
    payment_status = models.CharField(max_length=30, choices=STATUS, default='PENDING')
    payment_id = models.CharField(max_length=255, null=True)
    payment_response = models.JSONField(null=True)
    payment_mathod = models.CharField(max_length=30, null=True, choices=METHODS)
    payment_signature = models.CharField(max_length=255, null=True)
    payment_partner = models.CharField(max_length=30, null=True, choices=PAYMENT_PARTNER)
    created_at = models.DateTimeField(auto_now_add=True)
    time_slot = models.CharField(max_length=15, null=True, choices=TIMESLOT)
    payment_type = models.CharField(max_length=20, null=True)
    order_status = models.CharField(max_length=10, choices=DELIVERY_STATUS, default='PENDING', null=True, blank=True)


    objects = models.Manager()
    delivered = OrderManager()

    def save(self, *args, **kwargs):
        if not self.order_id :
            self.order_id = self.generate_id()
        super().save(*args, **kwargs)

    def generate_id(self) -> str:
        code = random.randint(298, 6897)
        code2 = random.randint(134, 4564)
        return f'FOOD{code}{code2}'

    def get_order_item(self):
        item = tiffines.Items.objects.filter(cart=self.cart.cart_id).first()
        return item

    def get_user_detail(self):
        return UserDetail.objects.get(user = self.user)

class UserDetail(models.Model):
    GENDER = (
        ('MALE', 'MALE'),
        ('FEMALE', 'FEMALE')
    )
    
    user =  models.OneToOneField(User, on_delete=models.CASCADE)
    altenate_number = models.CharField(max_length=12, null=True)
    phone = models.CharField(max_length=12)
    gender = models.CharField(max_length=10, null=True, choices=GENDER)            
    is_number_varified = models.BooleanField(default=False)



class EmailOrUsernameModelBackend(ModelBackend):
    """
    This is a ModelBacked that allows authentication
    with either a username or an email address.
    
    """
    def authenticate(self, username=None, password=None):
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = get_user_model().objects.get(**kwargs)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

    def get_user(self, username):
        try:
            return get_user_model().objects.get(pk=username)
        except get_user_model().DoesNotExist:
            return None