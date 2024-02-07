from django.db import models
from django.forms import ModelForm
from django import forms
from apps.models import User
from apps.utility import validate_phone_number


class UserRegisterForm(ModelForm):
    confirm_password = forms.CharField(max_length=25)

    class Meta:
        model = User
        fields = ['first_name', 'email', 'password', 'phone', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        phone = cleaned_data.get('phone')
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Parollar bir xil bo\'lishi kerak')
        if validate_phone_number(phone):
            raise forms.ValidationError('Telefon raqam xato')
        return cleaned_data




