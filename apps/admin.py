from django.contrib import admin
from django.contrib.auth.models import Group

from apps.models import Product, User, ProductImage


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ('name', 'description', 'price', 'quantity', 'is_in_stock')


admin.site.register(User)
admin.site.unregister(Group)
