from rest_framework import serializers
from tiffine_site.models import AddressModel


class AddressSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddressModel
        fields = ['user','street','locality','landmark','city','phone','pincode','created']

    def create(self, validated_data):
        return super().create(validated_data)