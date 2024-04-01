from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, CreateView

from apps.forms import OrderCreateForm
from apps.models import Product, Wishlist
from apps.models.product import Order


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
    model = Order
    form_class = OrderCreateForm
    template_name = 'apps/product/product-details.html'

    def form_invalid(self, form):
        super().form_invalid(form)
        slug = form.cleaned_data['product'].slug
        return redirect('product_detail', slug=slug)

    def form_valid(self, form):
        data = form.save()
        return redirect('success_product', data.id)


class OrderSuccessTemplateView(TemplateView):
    template_name = 'apps/product/order.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj: Order = get_object_or_404(Order.objects.all(), id=kwargs.get('pk'))
        # order = Order.objects.filter(id=kwargs.get('pk'))
        context['product'] = obj.product
        # print(obj.product.name)
        return context


class OrderListView(ListView):
    queryset = Order.objects.all()
    template_name = 'apps/product/order_list.html'
    context_object_name = 'orders'
    ordering = ('-id', )

    def get_queryset(self):
        return super().get_queryset().filter(status=Order.Status.NEW)





