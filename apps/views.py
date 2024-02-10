from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, CreateView, FormView, ListView, DetailView
from django.core.mail import send_mail

from apps.forms import UserRegisterForm, UserLoginForm
from apps.models import User, Product


class MainTemplateView(TemplateView):
    template_name = 'apps/index.html'


class ProfileTemplateView(TemplateView):
    template_name = 'apps/user/profile.html'


class SettingsTemplateView(TemplateView):
    template_name = 'apps/user/settings.html'


class ProductListView(ListView):
    model = Product
    template_name = 'apps/product/product-grid.html'
    context_object_name = 'products'
    paginate_by = 6


class ProductDetailView(DetailView):
    template_name = 'apps/product/product-details.html'
    model = Product
    context_object_name = 'product'
    slug_url_kwarg = 'slug'


class RegisterCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'apps/auth/register.html'
    success_url = '/'

    def form_valid(self, form):
        res = super().form_valid(form)
        email = form.cleaned_data.get('email')
        subject = 'test'
        message = 'test'
        from_email = 'ibrohim.dev.uz@gmail.com'
        recipient_list = [email]

        send_mail(subject, message, from_email, recipient_list)

        return res

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


class LoginFormView(FormView):
    form_class = UserLoginForm
    template_name = 'apps/auth/login.html'
    success_url = '/'

    def form_valid(self, form):
        phone = form.cleaned_data.get("phone")
        password = form.cleaned_data.get("password")
        # user = authenticate(self.request, username=phone, password=password)
        user = User.objects.filter(phone=phone, password=password).first()
        print(phone)
        print(password)
        print(user)
        if user:
            login(self.request, user)
            print('ok')
            return redirect('/')

        return super().form_valid(form)


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

