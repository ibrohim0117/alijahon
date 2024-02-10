from django.contrib.auth.hashers import make_password
from django.db import models
from django.forms import ModelForm
from django import forms
from apps.models import User
from apps.utility import validate_phone_number
from django import forms


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

    # def clean(self):
    #     cleaned_data = super().clean()
    #     phone = cleaned_data.get('phone')
    #     return cleaned_data


class UserLoginForm(forms.Form):
    phone = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)



