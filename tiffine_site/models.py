from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
import datetime
from django.db.models import F, Sum
import slugify
from django.urls import reverse
from datetime import datetime
import uuid



type_of = (
    ('VRG', 'VEG'),
    ('NON-VEG', 'NON-VEG'),
)


class MainDishModel(models.Model):
    name = models.CharField(max_length=100)
    deatil = models.CharField(max_length=255)
    price = models.FloatField()
    discounted = models.FloatField()
    availablity = models.BooleanField(default=True)
    image = models.ImageField(upload_to='pictures')
    ingredients = models.CharField(max_length=255)
    type_of = models.CharField(choices=type_of, max_length=10, blank=True)
    cabs = models.CharField(max_length=20, null=True, blank=True)
    protein = models.CharField(max_length=20, null=True, blank=True)
    fat = models.CharField(max_length=20, null=True, blank=True)
    fiber = models.CharField(max_length=20, null=True, blank=True)
    slug = models.SlugField(unique=True, null=True, blank=True)
    rating = models.FloatField(default=3.7, null=True)
    

    def __str__(self):
        return str(self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify.slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("deatail-view", kwargs={"slug": self.slug})
    


class AddToFevorate(models.Model):
    user = models.ForeignKey(
        User, related_name='user_fevorate', blank=True, null=True, on_delete=models.CASCADE)
    dish_name = models.ForeignKey(
        MainDishModel, related_name='dish_name', blank=True, null=True, on_delete=models.CASCADE)
    is_fav = models.BooleanField(default=False)


class CommentAndRating(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True, unique=False)
    dish = models.ForeignKey(
        MainDishModel, on_delete=models.SET_NULL, blank=True, null=True)
    is_show = models.BooleanField(default=True)
    comment = models.TextField(max_length=250)
    rating = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)


class AddressModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street = models.CharField(max_length=100, null=True, blank=True)
    locality = models.CharField(max_length=100, null=True, blank=True)
    landmark = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    phone = models.IntegerField(blank=True, null=True,)
    pincode = models.IntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        get_latest_by = ('-created', )
    
    def get_full_address(self):
        return f'{self.street} {self.locality} {self.landmark} {self.city}'
    
    def __str__(self) -> str:
        return f'{self.street} {self.locality}'

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart_id = models.CharField(max_length=20, blank=True, null=True)
    coupon_applied = models.PositiveIntegerField(default=0)
    coupond_amount = models.CharField(max_length=20, null=True, default=0)
    coupon_used = models.CharField(max_length=20, null=True)
    is_complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True)
    class Meta:
        get_latest_by = ('-created')

    def __str__(self) -> str:
        return self.cart_id
    
    def get_address(self):
        address_obj = AddressModel.objects.filter(user=self.user).first()
        return address_obj.get_full_address()

    def is_coupon_used(self):
        if self.coupon_applied != 0:
            return True

    def amount_plus(self):
        return self.item.discounted * self.quantity

    def save(self, *args, **kwargs):
        if not self.cart_id:
            self.cart_id = self.create_cart_id()
        return super(Cart, self).save(*args, **kwargs)

    def create_cart_id(self):
        return str(uuid.uuid4())[:10]

    def get_cart_items(self):
        return Items.objects.filter(cart=self.cart_id)

    def get_cart_price(self):
        try: 
            return float(self.get_cart_items().aggregate(total=Sum(F('food__discounted') * F('quantity')))['total'])
        except:
            return 0

    def get_delivery_amount(self):
        delivery_carge = DeliveryCharges.objects.filter(is_active=True).first()
        delivery_amount = 0
        if delivery_carge is not None:
            if self.get_cart_price() > 0:
                delivery_amount = delivery_carge.amount
            else:
                return delivery_amount

        final_amount = float(self.get_cart_price()) + float(delivery_amount)
        if self.coupon_applied == 1:
            return float(final_amount) - float(self.coupond_amount)
        else:
            return final_amount 

    def delivery_charge(self):
        delivery = DeliveryCharges.objects.filter(is_active=True).first()
        if delivery is not None:
            if self.get_cart_price() > 0:
                return float(delivery.amount)
            
        return 0

    def get_used_coupon(self):
        is_coupon = Coupon.objects.filter(coupon=self.coupon_used).first()
        if is_coupon is None:
            return False
        else:
            return is_coupon.mode

    def get_coupon_obj(self):
        coupon = Coupon.objects.filter(coupon=self.coupon_used).first()
        if coupon is None:
            return False
        else:
            return coupon

    def get_total_item_quantity(self):
        return self.get_cart_items().aggregate(count_total=Sum('quantity'))['count_total']
    
class Items(models.Model):
    cart = models.CharField(max_length=20)
    food = models.ForeignKey(MainDishModel, related_name='food', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    
    def item_price(self):
        return self.food.discounted * self.quantity

class Coupon(models.Model):
    TYPE = (
        ('VALUE', 'VALUE'),
        ('PERCENTAGE', 'PERCENTAGE')
    )
    MODE = (
        ('COD', 'COD'),
        ('ONLINE', 'ONLINE')
    )
    
    type_of = models.CharField(max_length=20, choices=TYPE)
    coupon = models.CharField(max_length=20)
    value = models.CharField(max_length=20)
    validity = models.DateTimeField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    mode = models.CharField(max_length=20, default='ONLINE', choices=MODE)
    active = models.BooleanField(default=False)

    def check_coupon_validity(self):
        if self.validity.date() > datetime.now().date():
            return True
        return False
    

class OrderDetails(models.Model):
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.SET_NULL, editable=False)

    item_1 = models.ForeignKey(
        MainDishModel, blank=True, related_name='item_1', null=True, on_delete=models.SET_NULL, editable=False)
    qyt_1 = models.PositiveIntegerField(
        blank=True,  null=True, editable=False, )

    item_2 = models.ForeignKey(
        MainDishModel, blank=True, related_name='item_2', null=True, on_delete=models.SET_NULL, editable=False)
    qyt_2 = models.PositiveIntegerField(blank=True,  null=True, editable=False)

    item_3 = models.ForeignKey(
        MainDishModel, blank=True, related_name='item_3', null=True, on_delete=models.SET_NULL, editable=False)
    qyt_3 = models.PositiveIntegerField(
        blank=True, null=True, editable=False, )

    item_4 = models.ForeignKey(
        MainDishModel, blank=True, related_name='item_4', null=True, on_delete=models.SET_NULL, editable=False)
    qyt_4 = models.PositiveBigIntegerField(
        blank=True, null=True, editable=False, )

    item_5 = models.ForeignKey(
        MainDishModel, blank=True, related_name='item_5', null=True, on_delete=models.SET_NULL, editable=False)
    qyt_5 = models.PositiveBigIntegerField(
        blank=True, null=True, editable=False, )

    order_id = models.CharField(
        max_length=100, blank=True, null=True, editable=False)
    payment_id = models.CharField(
        max_length=100, blank=True, null=True, editable=False)
    date_time = models.DateTimeField(
        default=timezone.now, blank=True, null=True, editable=False)
    amount = models.FloatField(blank=True, null=True, editable=False)
    upi_transaction_id = models.CharField(
        max_length=100, blank=True, null=True, editable=False)
    vpa = models.CharField(max_length=100, blank=True,
                           null=True, editable=False)
    card_id = models.CharField(
        max_length=100, blank=True, null=True, editable=False)
    bank = models.CharField(max_length=100, blank=True,
                            null=True, editable=False)
    method = models.CharField(
        max_length=100, blank=True, null=True, editable=False)
    wallet = models.CharField(
        max_length=100, blank=True, null=True, editable=False)

        
class DeliveryCharges(models.Model):
    amount = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=False)


class CustomersFavorite(models.Model):
    product = models.ForeignKey(MainDishModel, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)



class PeopleFavorite(models.Model):
    LOCATION = (
        ('CART', 'CART'),
        ('MENU', 'MENU')
    )
    
    food = models.ManyToManyField(MainDishModel)
    location = models.CharField(max_length=20, choices=LOCATION)