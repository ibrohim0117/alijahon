from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    image = models.ImageField(upload_to='users/images/', null=True, blank=True, default='apps/assets/img/logo.png')
    phone = models.CharField(max_length=25)
    email = models.EmailField(unique=True)  # Add unique=True here

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # def save(self, *args, **kwargs):
    #     first_name = self.first_name
    #     print(first_name)
    #
    #     return super().save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='products/images/')
    price = models.FloatField()

    class Meta:
        verbose_name = 'Mahsulot'
        verbose_name_plural = 'Mahsulotlar'

    def __str__(self):
        return self.name

