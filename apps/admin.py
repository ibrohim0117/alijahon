from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import Group

from apps.models import Product, User

admin.site.register(Product)
admin.site.register(User)

admin.site.unregister(Group)
