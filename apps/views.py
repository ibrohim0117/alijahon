from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import TemplateView, CreateView, FormView, ListView, DetailView, UpdateView

from apps.forms import UserRegisterForm, UserLoginForm, WishlistForm, UserUpdateProfileForm
from apps.models import User, Product, Wishlist
from apps.tasks import task_send_mail


class MainTemplateView(TemplateView):
    template_name = 'apps/index.html'


class ProfileTemplateView(TemplateView):
    template_name = 'apps/user/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context['user'] = user
        return context


class SettingsTemplateView(TemplateView):
    template_name = 'apps/user/settings.html'


class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = 'apps/product/product-grid.html'
    context_object_name = 'products'
    paginate_by = 6
    ordering = ('-id', )


class ProductDetailView(DetailView):
    template_name = 'apps/product/product-details.html'
    model = Product
    context_object_name = 'product'
    slug_url_kwarg = 'slug'


class WishlistCreateView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        user = self.request.user
        slug = self.kwargs.get('slug')
        product = Product.objects.filter(slug=slug).first()
        if user and slug:
            if not Wishlist.objects.filter(product=product).exists():
                Wishlist.objects.create(
                    user=user,
                    product=product
                )
            else:
                wishlist = Wishlist.objects.filter(product=product).first()
                wishlist.delete()
        return redirect('/')


class WishlistRemoveView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        product = Product.objects.filter(slug=slug).first()
        wishlist = Wishlist.objects.filter(product=product).first()
        wishlist.delete()
        return redirect('/')


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


class UpdateViewProfile(UpdateView):
    model = User
    form_class = UserUpdateProfileForm
    template_name = 'apps/user/profile.html'
    success_url = '/'


class ConfirmMailTemplateView(TemplateView):
    template_name = 'apps/auth/confirm-mail.html'


class ForgetPasswordTemplateView(TemplateView):
    template_name = 'apps/auth/forgot-password.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class LockScreenTemplateView(TemplateView):
    template_name = 'apps/auth/lock-screen.html'


class LogoutRedirectView(View):
    def get(self, *args, **kwargs):
        logout(self.request)
        return redirect('/')


class ResetPasswordTemplateView(TemplateView):
    template_name = 'apps/auth/reset-password.html'


class ShoppingListView(ListView):
    template_name = 'apps/product/shopping-cart.html'
    queryset = Wishlist.objects.all()
    context_object_name = 'wishlists'
    ordering = ('-id',)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)



