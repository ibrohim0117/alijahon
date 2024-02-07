from django.contrib import admin
from django.contrib.auth.models import Group

from apps.models import Product, User, ProductImage, Wishlist, Category


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 1


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    search_fields = ('name', 'description', 'price')
    list_display = ('name', 'description', 'price', 'quantity', 'specifications', 'is_in_stock')


@admin.register(User)
class UserModelAdmin(admin.ModelAdmin):
    search_fields = ('phone', )


admin.site.register(Wishlist)
admin.site.register(Category)


admin.site.unregister(Group)
