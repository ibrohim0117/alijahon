from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db.models import ForeignKey, CASCADE, DateTimeField, ImageField, CharField, EmailField, Model, TextField, \
    PositiveIntegerField, SlugField
from django.forms import FloatField
from jsonfield import JSONField
from django.utils.text import slugify


class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('The Phone Number field must be set')

        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(phone, password, **extra_fields)


class BaseModel(Model):
    created_at = DateTimeField(auto_now_add=True)
    update_at = DateTimeField(auto_now=True)


# proxymodel
class User(AbstractUser, BaseModel):

    TEXT_CHOICES = [
        (0, 'Users'),
        (1, 'Admin'),
        (2, 'Couriers'),
        (3, 'Managers'),
        (4, 'Operators'),
        (5, 'Spams')
    ]

    text_choice = CharField(
        max_length=20,
        choices=TEXT_CHOICES,
        default='0',
    )

    image = ImageField(upload_to='users/images/', null=True, blank=True, default='apps/assets/img/logo.png')
    phone = CharField(max_length=25, unique=True)
    email = EmailField(unique=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    username = None


class ProductCategoryModel(Model, BaseModel):
    name = CharField(max_length=25)


class Product(Model):
    name = CharField(max_length=255)
    description = TextField()
    price = FloatField()
    quantity = PositiveIntegerField(default=0)
    specifications = JSONField(default=dict)
    slug = SlugField(unique=True, max_length=255, blank=True, null=True)
    category = ForeignKey('apps.ProductCategoryModel', CASCADE, on_delete=True)

    class Meta:
        verbose_name = 'Mahsulot'
        verbose_name_plural = 'Mahsulotlar'

    def __str__(self):
        return self.name

    @property
    def is_in_stock(self):
        return self.quantity > 0

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class ProductImage(Model, BaseModel):
    product = ForeignKey(Product, CASCADE, related_name='images')
    image = ImageField(upload_to='products/images/')

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'Mahsulot rasmi'
        verbose_name_plural = 'Mahsulotlar rasmlari'


class Wishlist(Model, BaseModel):
    user = ForeignKey('apps.User', CASCADE)
    product = ForeignKey('apps.Product', CASCADE, on_delete=True)
    updated_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True)