import uuid
from datetime import timedelta
from ckeditor.fields import RichTextField
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db.models import ForeignKey, CASCADE, DateTimeField, ImageField, CharField, EmailField, Model, TextField, \
    PositiveIntegerField, SlugField, TextChoices, FloatField, IntegerField
from django.utils.timezone import now
from django_resized import ResizedImageField
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

    class Meta:
        abstract = True


class User(AbstractUser):
    class Type(TextChoices):
        USERS = 0, 'Users'
        ADMIN = 1, 'Admin'
        COURIER = 2, 'Couriers'
        MANAGER = 3, 'Managers'
        OPERATOR = 4, 'Operators'

    type = CharField(max_length=20, choices=Type.choices, default=Type.USERS)
    image = ImageField(upload_to='users/images/', null=True, blank=True, default='users/images/user.jpg')
    phone_regex = RegexValidator(regex=r'^\+998\d{9}$|^\d{9}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 25 digits allowed.")
    phone = CharField(max_length=25, unique=True, validators=[phone_regex])
    email = EmailField(unique=True, null=True, blank=True)
    viloyat = CharField(max_length=25, blank=True, null=True)
    shahar = CharField(max_length=25, blank=True, null=True)
    address = CharField(max_length=25, blank=True, null=True)
    about_me = TextField()

    objects = CustomUserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    username = None

    class Meta:
        verbose_name = 'Foydalanuvchi'
        verbose_name_plural = 'Foydalanuvchilar'

    @property
    def wishlist_summa(self):
        return sum(self.wishlist_set.values_list('product__price', flat=True))

    @property
    def wishlist_count(self):
        return self.wishlist_set.count()


class Category(BaseModel):
    name = CharField(max_length=25)

    class Meta:
        verbose_name = 'Kategorya'
        verbose_name_plural = 'Kategoryalar'

    def __str__(self):
        return self.name


class Product(BaseModel):
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

    @property
    def is_new(self):
        return now() - timedelta(days=7) < self.created_at

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if Product.objects.filter(slug=self.slug).exists():
            self.slug += uuid.uuid4.__str__().split('-')[-1]
        super().save(*args, **kwargs)


class ProductImage(BaseModel):
    product = ForeignKey(Product, CASCADE, related_name='images')
    image = ResizedImageField(upload_to='products/images/', size=[1000, 800], crop=['middle', 'center'])

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'Mahsulot rasmi'
        verbose_name_plural = 'Mahsulotlar rasmlari'


class Wishlist(BaseModel):
    user = ForeignKey('apps.User', CASCADE)
    product = ForeignKey('apps.Product', CASCADE)

    def __str__(self):
        return self.product.name

    class Meta:
        verbose_name = 'Buyurtma'
        verbose_name_plural = 'Buyurtmalar'


class Order(BaseModel):
    product_name = CharField(max_length=255)
    quantity = IntegerField(default=0)
