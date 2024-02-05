from django.db import models
from django.forms import ModelForm
from django import forms
from apps.models import User


class UserRegisterForm(ModelForm):
    confirm_password = forms.CharField(max_length=25)

    class Meta:
        model = User
        fields = ['first_name', 'email', 'password', 'phone', 'confirm_password']

    def clean(self):
        print(self.cleaned_data)
        print(self.data)

