from django.contrib import sitemaps
from tiffine_site.models import MainDishModel


class FoodSiteMap(sitemaps.Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return MainDishModel.objects.all()