from django.db import models
from tiffine_site import models as tiffines
from django.urls import reverse     

# Create your models here.
class BannersModel(models.Model):
    BANNERS = (
        ('HOME_CAROSEL' , 'HOME_CAROSEL'),
        ('MENU_CAROCEL' , 'MENU_CAROCEL'),
        ('CART_IMG' , 'CART_IMG'),
        ('ADDRESS_IMG', 'ADDRESS_IMG'),
        ('PAYMENT_IMG' , 'PAYMENT_IMG'),
        ('ADDRESS-COUPON', 'ADDRESS-COUPON')
    )

    itmes = models.ForeignKey(tiffines.MainDishModel, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='products', null=True)
    validity = models.DateTimeField(blank=True, null=True)
    banner_type = models.CharField(max_length=25, choices=BANNERS, null=True)
    text = models.TextField(null=True, blank=True)
    crested_at = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse("deatail-view", kwargs={"slug": self.itmes.slug})