from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import AddressModel
from django.forms import ModelForm, Textarea
from django.core.exceptions import ValidationError



class AddressForm(forms.ModelForm):
    class Meta:
        model = AddressModel
        fields = ('street', 'locality', 'landmark', 'city', 'phone', 'pincode')
        widgets = {
            'street': forms.TextInput(attrs={'class': 'form-control', 'id': 'street-id'}),
            'locality': forms.TextInput(attrs={'class': 'form-control', 'id': 'locality-id'}),
            'landmark': forms.TextInput(attrs={'class': 'form-control', 'id': 'landmark-id'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'id': 'city-id'}),
            'phone': forms.NumberInput(attrs={'class': 'form-control', 'id': 'phone-id'}),
            'pincode': forms.NumberInput(attrs={'class': 'form-control', 'id': 'pincode-id'}),
        }


class CustomUserCreationForm(UserCreationForm):  
    username = forms.CharField(label='Username', min_length=5, max_length=150)  
    email = forms.EmailField(label='Email')  
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)  
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)  
  
    def username_clean(self):  
        username = self.cleaned_data['username'].lower()  
        new = User.objects.filter(username = username)  
        if new.count():  
            raise ValidationError("User Already Exist")  
        return username  
  
    def email_clean(self):  
        email = self.cleaned_data['email'].lower()  
        new = User.objects.filter(email=email)  
        if new.count():  
            raise ValidationError(" Email Already Exist")  
        return email  
  
    def clean_password2(self):  
        password1 = self.cleaned_data['password1']  
        password2 = self.cleaned_data['password2']  
  
        if password1 and password2 and password1 != password2:  
            raise ValidationError("Password don't match")  
        return password2  
  
    def save(self, commit = True):  
        user = User.objects.create_user(  
            self.cleaned_data['username'],  
            self.cleaned_data['email'],  
            self.cleaned_data['password1']  
        )  
        return user  