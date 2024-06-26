from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q, Sum
from django.shortcuts import redirect, get_object_or_404, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, CreateView, UpdateView, FormView

from apps.forms import OrderCreateForm, OrderUpdateModelForm, StreamCreateForm
from apps.mixins import NotOperatorRequiredMixin
from apps.models import Product, Wishlist
from apps.models.product import Order, Region, Stream


class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = 'apps/product/product-grid.html'
    context_object_name = 'products'
    paginate_by = 6
    ordering = ('-id', )

    def get_queryset(self):
        name = self.request.GET.get('search')
        qs = super().get_queryset()
        if name is not None and len(name) > 0:
            qs = qs.filter(name__icontains=name)

        return qs


class ProductDetailView(DetailView):
    template_name = 'apps/product/product-details.html'
    model = Product
    context_object_name = 'product'

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)  # stream
        slug = self.kwargs.get(self.slug_url_kwarg)  # product
        if pk:
            stream = get_object_or_404(Stream.objects.all(), pk=pk)
            stream.count += 1
            stream.save()
            return stream.product
        return get_object_or_404(Product.objects.all(), slug=slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stream_id'] = self.kwargs.get(self.pk_url_kwarg, '')
        return context


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


class ShoppingListView(LoginRequiredMixin, ListView):
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
        order = form.save(False)
        order.user = self.request.user
        order.save()
        return redirect('success_product', order.id)


class OrderSuccessTemplateView(TemplateView):
    template_name = 'apps/product/order_success.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj: Order = get_object_or_404(Order.objects.all(), id=kwargs.get('pk'))
        # order = Order.objects.filter(id=kwargs.get('pk'))
        context['product'] = obj.product
        # print(obj.product.name)
        return context


class OrderListView(LoginRequiredMixin, ListView):
    queryset = Order.objects.filter(status=Order.Status.NEW)
    template_name = 'apps/product/order_list.html'
    context_object_name = 'orders'

    def get_object(self, queryset=None):
        order_id = self.request.POST.get('order_id')
        return get_object_or_404(Order.objects.all(), pk=order_id)

    def post(self, request, *args, **kwargs):
        order = self.get_object()
        order.operator = request.user
        order.save()
        return redirect('order_update', order.pk)


class BaseOperatorListView(NotOperatorRequiredMixin, ListView):
    queryset = Order.objects.all()
    template_name = 'apps/product/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return super().get_queryset().filter(operator=self.request.user)


class OrderREADYTODELIVERYListView(BaseOperatorListView):
    def get_queryset(self):
        return super().get_queryset().filter(status=Order.Status.READY_TO_DELIVERY)


class OrderARCHIVEListView(BaseOperatorListView):
    def get_queryset(self):
        return super().get_queryset().filter(status=Order.Status.ARCHIVE)


class OrderDELIVEREDListView(BaseOperatorListView):
    def get_queryset(self):
        return super().get_queryset().filter(status=Order.Status.DELIVERED)


class OrderBROKENListView(BaseOperatorListView):
    def get_queryset(self):
        return super().get_queryset().filter(status=Order.Status.BROKEN)


class OrderRETURNEDListView(BaseOperatorListView):
    def get_queryset(self):
        return super().get_queryset().filter(status=Order.Status.RETURNED)


class OrderCANCELLEDListView(BaseOperatorListView):
    def get_queryset(self):
        return super().get_queryset().filter(status=Order.Status.CANCELLED)


class OrderWAITINGListView(BaseOperatorListView):
    def get_queryset(self):
        return super().get_queryset().filter(status=Order.Status.WAITING)


class OrderUpdateView(LoginRequiredMixin, UpdateView):
    model = Order
    form_class = OrderUpdateModelForm
    template_name = 'apps/product/order_update.html'
    success_url = reverse_lazy('order_list')

    def get_context_data(self, **kwargs):
        contex = super().get_context_data(**kwargs)
        self.get_object()
        # order = Order.objects.filter(id=self.kwargs.get('pk')).first()
        # contex['order'] = order
        contex['regions'] = Region.objects.all()
        return contex


class MarketListView(LoginRequiredMixin, ListView):
    queryset = Product.objects.all()
    template_name = 'apps/product/market.html'
    context_object_name = 'products'
    ordering = ['-created_at']


class StreamFormView(LoginRequiredMixin, FormView):
    form_class = StreamCreateForm
    template_name = 'apps/product/market.html'

    def form_valid(self, form):
        stream = form.save(False)
        stream.user = self.request.user
        stream.save()
        return redirect('market')



class StreamListView(LoginRequiredMixin, TemplateView):
    # queryset = Stream.objects.all()
    template_name = 'apps/product/stream-list.html'
    # context_object_name = 'streams'
    #
    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class StreamDetailView(DetailView):
    model = Stream
    template_name = 'apps/product/product-details.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        stream = get_object_or_404(Stream.objects.all(), pk=pk)
        return stream.product


class StatistikaListView(LoginRequiredMixin, ListView):
    queryset = Stream.objects.annotate(
        yangi=Count('orders', filter=Q(orders__status=Order.Status.NEW)),
        arxivlandi=Count('orders', filter=Q(orders__status='arxivlandi')),
        yetkazishga_tayyor=Count('orders', filter=Q(orders__status='yetkazishga_tayyor')),
        yetkazildi=Count('orders', filter=Q(orders__status='yetkazildi')),
        kiyin_oladi=Count('orders', filter=Q(orders__status='kiyin_oladi')),
        bekor_qilindi=Count('orders', filter=Q(orders__status='bekor_qilindi'))
    ).select_related('product')
    template_name = 'apps/product/statistika.html'
    context_object_name = 'streams'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        qs = self.get_queryset()
        context.update(**qs.aggregate(
            visit_total=Sum('count'),
            yangi_total=Sum('yangi'),
            arxivlandi_total=Sum('arxivlandi'),
            yetkazishga_tayyor_total=Sum('yetkazishga_tayyor'),
            yetkazildi_total=Sum('yetkazildi'),
            kiyin_oladi_total=Sum('kiyin_oladi'),
            bekor_qilindi_total=Sum('bekor_qilindi'),
        ))
        return context


class MyOrdersListView(LoginRequiredMixin, ListView):
    queryset = Order.objects.all()
    template_name = 'apps/product/my_orders.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class SurovlarListView(LoginRequiredMixin, ListView):
    queryset = Order.objects.all()
    template_name = 'apps/product/surovlar.html'
    context_object_name = 'aktiv_list'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

# Stream.objects.annotate(new_count=Count('orders', filter=Q(orders__status='yangi')),
# cancel_count=Count('orders', filter=Q(orders__status='arxivlandi'))).values('name', 'product__name', 'count', 'new_count', 'cancel_count')







