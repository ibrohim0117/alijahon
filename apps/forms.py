from django import forms
from django.contrib.auth.hashers import make_password
from django.forms import ModelForm
from django.shortcuts import get_object_or_404

from apps.models import Product
from apps.models.user import User
from apps.models.product import Order, Wishlist


class UserRegisterForm(ModelForm):
    confirm_password = forms.CharField(max_length=25)

    class Meta:
        model = User
        fields = ['first_name', 'email', 'password', 'phone', 'confirm_password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Parollar bir xil bo\'lishi kerak')
        return make_password(password)


class UserUpdateProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'viloyat', 'shahar', 'address', 'about_me']


class UserLoginForm(forms.Form):
    phone = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = ['user', 'product']


class OrderCreateForm(ModelForm):
    class Meta:
        model = Order
        fields = ['full_name', 'phone', 'product']

    def validate_product(self):
        slug = self.cleaned_data.get('product')
        product = get_object_or_404(Product.objects.all(), slug=slug)
        return product.id



