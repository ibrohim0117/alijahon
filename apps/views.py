from django.shortcuts import render
from django.views.generic import TemplateView, CreateView

from apps.forms import UserRegisterForm
from apps.models import User


class MainTemplateView(TemplateView):
    template_name = 'apps/index.html'


class ProfileTemplateView(TemplateView):
    template_name = 'apps/user/profile.html'


class SettingsTemplateView(TemplateView):
    template_name = 'apps/user/settings.html'


class ProductTemplateView(TemplateView):
    template_name = 'apps/product/product-grid.html'


class ProductDetailsTemplateView(TemplateView):
    template_name = 'apps/product/product-details.html'


class RegisterTemplateView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'apps/auth/register.html'
    success_url = '/'

# def RegisterTemplateView(requests):
#     if requests.POST:
#         data = UserRegisterForm(requests.POST)
#         password = requests.POST.get('password')
#         confirm_password = requests.POST.get('confirm_password')
#         if password == confirm_password:
#             if data.is_valid():
#                 data.save()
#                 print('Ishladi')
#     return render(requests, 'apps/auth/register.html')


class LoginTemplateView(TemplateView):
    template_name = 'apps/auth/login.html'


class ConfirmMailTemplateView(TemplateView):
    template_name = 'apps/auth/confirm-mail.html'


class ForgetPasswordTemplateView(TemplateView):
    template_name = 'apps/auth/forgot-password.html'


class LockScreenTemplateView(TemplateView):
    template_name = 'apps/auth/lock-screen.html'


class LogoutTemplateView(TemplateView):
    template_name = 'apps/auth/lock-screen.html'


class ResetPasswordTemplateView(TemplateView):
    template_name = 'apps/auth/reset-password.html'

