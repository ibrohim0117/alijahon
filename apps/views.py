from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.views import View
from django.views.generic import TemplateView, CreateView, FormView, ListView, DetailView
from apps.forms import UserRegisterForm, UserLoginForm
from apps.models import User, Product
from apps.tasks import task_send_mail


class MainTemplateView(TemplateView):
    template_name = 'apps/index.html'


class ProfileTemplateView(TemplateView):
    template_name = 'apps/user/profile.html'


class SettingsTemplateView(TemplateView):
    template_name = 'apps/user/settings.html'


class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = 'apps/product/product-grid.html'
    context_object_name = 'products'
    paginate_by = 3
    ordering = ('-id', )


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
        task_send_mail.delay(email)
        return res


class LoginFormView(FormView):
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


class ConfirmMailTemplateView(TemplateView):
    template_name = 'apps/auth/confirm-mail.html'


class ForgetPasswordTemplateView(TemplateView):
    template_name = 'apps/auth/forgot-password.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class LockScreenTemplateView(TemplateView):
    template_name = 'apps/auth/lock-screen.html'


class LogoutRedirectView(View):
    # template_name = 'apps/auth/lock-screen.html'
    # next_page = reverse_lazy('login')
    def get(self, *args, **kwargs):
        logout(self.request)
        return redirect('login')


class ResetPasswordTemplateView(TemplateView):
    template_name = 'apps/auth/reset-password.html'

