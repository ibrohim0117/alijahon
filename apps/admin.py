from django.contrib import admin
from django.contrib.auth.models import Group

from apps.models import Product, ProductImage, Category
from apps.models.product import Order, Stream
from apps.proxy import UserProxy, CouriersProxy, AdminProxy, OperatorProxy, MangerProxyModel


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    exclude = ('slug',)
    search_fields = ('name', 'description', 'price')
    list_display = ('name', 'description', 'price', 'quantity', 'specifications', 'is_in_stock')


@admin.register(UserProxy)
class UserModelAdmin(admin.ModelAdmin):
    search_fields = ('phone', )


@admin.register(CouriersProxy)
class CourierModelAdmin(admin.ModelAdmin):
    search_fields = ('phone', )


@admin.register(AdminProxy)
class AdminProxyModel(admin.ModelAdmin):
    search_fields = ('phone', )


@admin.register(OperatorProxy)
class OperatorModelAdmin(admin.ModelAdmin):
    search_fields = ('phone', )


@admin.register(MangerProxyModel)
class ManagerModelAdmin(admin.ModelAdmin):
    search_fields = ('phone', )


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'quantity', 'phone')


admin.site.register(Stream)
admin.site.register(Category)
admin.site.unregister(Group)
