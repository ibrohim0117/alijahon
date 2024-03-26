from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, CreateView

from apps.forms import OrderCreateForm
from apps.models import Product, Wishlist


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


class ShoppingListView(ListView):
    template_name = 'apps/product/shopping-cart.html'
    queryset = Wishlist.objects.all()
    context_object_name = 'wishlists'
    ordering = ('-id',)

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class OrderCreateView(CreateView):
    form_class = OrderCreateForm
    template_name = 'apps/product/product-details.html'

    def form_valid(self, form):
        super().form_valid(form)
        return redirect('success_product')

    def form_invalid(self, form):
        super().form_invalid(form)
        print(form.cleaned_data)
        return redirect('product_detail', slug='123')

    # def post(self, request, *args, **kwargs):
    #     super().post(request, *args, **kwargs)
    #     return redirect('success_product')


class OrderSuccessTemplateView(TemplateView):
    template_name = 'apps/product/order.html'