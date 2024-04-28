import uuid
from datetime import timedelta
from ckeditor.fields import RichTextField
from django.core.validators import RegexValidator
from django.utils.timezone import now
from django_resized import ResizedImageField
from jsonfield import JSONField
from django.utils.text import slugify
from django.db.models import (
    ForeignKey, CASCADE, DateTimeField,
    CharField, Model, PositiveIntegerField,
    SlugField, FloatField, IntegerField, TextChoices, SET_NULL, Count
)


class BaseModel(Model):
    created_at = DateTimeField(auto_now_add=True)
    update_at = DateTimeField(auto_now=True)

    class Meta:
        abstract = True


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
            self.slug += uuid.uuid4().__str__().split('-')[-1]
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


class Region(Model):
    name = CharField(max_length=30)


class District(Model):
    name = CharField(max_length=30)
    region = ForeignKey('apps.Region', CASCADE)


class Order(BaseModel):

    class Status(TextChoices):
        NEW = 'yangi', 'Yangi'
        ARCHIVE = 'arxivlandi', 'Arxivlandi'
        DELIVERED = 'yetkazildi', 'Yetkazildi'
        BROKEN = 'nosoz_mahsukot', 'Nosoz mahsukot'
        RETURNED = 'qaytib_keldi', 'Qaytib keldi'
        CANCELLED = 'bekor_qilindi', 'Bekor qilindi'
        WAITING = 'kiyin_oladi', 'Kiyin oladi'
        READY_TO_DELIVERY = 'yetkazishga_tayyor', 'Yetkazishga tayyor'

    full_name = CharField(max_length=255)
    quantity = IntegerField(default=0)
    phone_regex = RegexValidator(regex=r'^\+998\d{9}$|^\d{9}$',
                                 message="Phone number must be entered  in the format: '+999999999'. Up to 25 digits allowed.")
    phone = CharField(max_length=25, validators=[phone_regex])
    product = ForeignKey('apps.Product', CASCADE, to_field='slug', related_name='product')
    status = CharField(max_length=20, choices=Status.choices, default=Status.NEW)
    referral_user = ForeignKey('apps.User', CASCADE, 'referral', blank=True, null=True, verbose_name='Referal foydalanuvchi')
    user = ForeignKey('apps.User', CASCADE, 'user', blank=True, null=True, verbose_name='Foydalanuvchi')
    comment = CharField(max_length=255, blank=True, null=True)
    region = ForeignKey('apps.Region', CASCADE, verbose_name='Viloyat', blank=True, null=True)
    stream = ForeignKey('apps.Stream', SET_NULL, blank=True, null=True, related_name='orders')
    district = ForeignKey('apps.District', CASCADE, verbose_name='Tuman', blank=True, null=True)
    street = CharField(max_length=25, verbose_name="Ko'cha", blank=True, null=True)
    operator = ForeignKey('apps.User', CASCADE, 'operator', blank=True, null=True, verbose_name='Operator')

    class Meta:
        ordering = ['id']
        verbose_name = 'Zakaz'
        verbose_name_plural = 'Zakazlar'

    def __str__(self):
        return self.product.name

    @property
    def is_ready_to_delivery(self):
        return


class Stream(BaseModel):
    name = CharField(max_length=25)
    user = ForeignKey('apps.User', CASCADE)
    count = IntegerField(default=0)
    product = ForeignKey('apps.Product', CASCADE, related_name='streams')

    class Meta:
        verbose_name = 'Oqim'
        verbose_name_plural = 'Oqimlar'

    def __str__(self):
        return f'{self.product.name} --> {self.user}'








