from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db.models import DateTimeField, ImageField, CharField, EmailField, Model, TextField, \
    TextChoices


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
    viloyat = CharField(max_length=25, blank=True, null=True)    # noqa
    shahar = CharField(max_length=25, blank=True, null=True)    # noqa
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
