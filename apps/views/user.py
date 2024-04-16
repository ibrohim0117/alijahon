from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, FormView, UpdateView

from apps.forms import UserRegisterForm, UserLoginForm, UserUpdateProfileForm
from apps.mixins import NotLoginRequiredMixin
from apps.models import User
from apps.tasks import task_send_mail


class MainTemplateView(TemplateView):
    template_name = 'apps/index.html'


class ProfileTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'apps/user/profile.html'
    login_url = reverse_lazy('login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        return context


class SettingsTemplateView(TemplateView):
    template_name = 'apps/user/settings.html'


class RegisterCreateView(NotLoginRequiredMixin, CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'apps/auth/register.html'
    success_url = '/'

    def form_valid(self, form):
        res = super().form_valid(form)
        email = form.cleaned_data.get('email')
        task_send_mail.delay(email)
        return res


class LoginFormView(NotLoginRequiredMixin, FormView):
    form_class = UserLoginForm
    template_name = 'apps/auth/login.html'
    success_url = '/'

    def form_valid(self, form):
        phone = form.cleaned_data.get("phone")
        password = form.cleaned_data.get("password")
        user = User.objects.filter(phone=phone).first()
        if user and user.check_password(password):
            login(self.request, user)
            return redirect('/')
        return super().form_valid(form)


class UpdateViewProfile(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserUpdateProfileForm
    template_name = 'apps/user/profile.html'
    success_url = '/'
    login_url = reverse_lazy('login')

    def get_object(self, queryset=None):
        return self.request.user


class ConfirmMailTemplateView(TemplateView):
    template_name = 'apps/auth/confirm-mail.html'


class ForgetPasswordTemplateView(TemplateView):
    template_name = 'apps/auth/forgot-password.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class LockScreenTemplateView(TemplateView):
    template_name = 'apps/auth/lock-screen.html'


class LogoutRedirectView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        logout(self.request)
        return redirect('/')


class ResetPasswordTemplateView(TemplateView):
    template_name = 'apps/auth/reset-password.html'






