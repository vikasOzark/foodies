from rest_framework import serializers
from tiffine_site import models
from django.contrib.auth.models import User
from . models import UserDetail



class AddressSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.AddressModel
        fields = '__all__'
    

class UserDetailSerializers(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = UserDetail
        fields = '__all__'