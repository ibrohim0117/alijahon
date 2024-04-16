from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.forms import ModelForm, ModelChoiceField, CharField, Form, PasswordInput, ChoiceField
from django.forms.utils import ErrorList

from apps.models import Product
from apps.models.user import User
from apps.models.product import Order, Wishlist, Stream


class UserRegisterForm(ModelForm):
    confirm_password = CharField(max_length=25)

    class Meta:
        model = User
        fields = ['first_name', 'email', 'password', 'phone', 'confirm_password']

    def clean_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise ValidationError('Parollar bir xil bo\'lishi kerak')
        return make_password(password)


class UserUpdateProfileForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'viloyat', 'shahar', 'address', 'about_me']


class UserLoginForm(Form):
    phone = CharField(max_length=100)
    password = CharField(widget=PasswordInput)


class WishlistForm(ModelForm):
    class Meta:
        model = Wishlist
        fields = ['user', 'product']


class OrderCreateForm(ModelForm):

    class Meta:
        model = Order
        fields = ['full_name', 'phone', 'product']


class StreamCreateForm(ModelForm):
    product = ModelChoiceField(queryset=Product.objects.all())
    class Meta:
        model = Stream
        fields = ['name', 'product']


class OrderUpdateModelForm(ModelForm):
    class Meta:
        model = Order
        fields = ['quantity', 'region', 'status', 'comment']


