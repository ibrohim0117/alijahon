from ckeditor.fields import RichTextField
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db.models import ForeignKey, CASCADE, DateTimeField, ImageField, CharField, EmailField, Model, TextField, \
    PositiveIntegerField, SlugField, TextChoices, FloatField
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


class BaseModel:
    created_at = DateTimeField(auto_now_add=True)
    update_at = DateTimeField(auto_now=True)


# proxymodel
class User(AbstractUser):
    class Type(TextChoices):
        Users = 0, 'Users'
        Admin = 1, 'Admin'
        Couriers = 2, 'Couriers'
        Managers = 3, 'Managers'
        Operators = 4, 'Operators'
        Spams = 5, 'Spams'

    text_choice = CharField(
        max_length=20,
        choices=Type.choices,
        default=Type.Users,
    )

    image = ImageField(upload_to='users/images/', null=True, blank=True, default='apps/assets/img/logo.png')
    phone = CharField(max_length=25, unique=True)
    email = EmailField(unique=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    username = None

    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'


class Category(BaseModel, Model):
    name = CharField(max_length=25)

    class Meta:
        verbose_name = 'Kategorya'
        verbose_name_plural = 'Kategoryalar'

    def __str__(self):
        return self.name


class Product(BaseModel, Model):
    name = CharField(max_length=255)
    description = RichTextField()
    price = FloatField()
    quantity = PositiveIntegerField(default=0)
    specifications = JSONField(default=dict)
    slug = SlugField(unique=True, max_length=255, blank=True, null=True)
    category = ForeignKey('apps.Category', CASCADE)

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


class ProductImage(BaseModel, Model):
    product = ForeignKey(Product, CASCADE, related_name='images')
    image = ImageField(upload_to='products/images/')

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'Mahsulot rasmi'
        verbose_name_plural = 'Mahsulotlar rasmlari'


class Wishlist(BaseModel, Model):
    user = ForeignKey('apps.User', CASCADE)
    product = ForeignKey('apps.Product', CASCADE)

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'Buyurtma'
        verbose_name_plural = 'Buyurtmalar'
