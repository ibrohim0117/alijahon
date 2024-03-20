from django.template import Library

from apps.models import Wishlist

register = Library()


@register.filter("custom_slice", is_safe=True)
def custom_slice_filter(value, arg: str):
    a, b = map(int, arg.split(':'))
    return list(value)[a: b]


@register.filter()
def is_liked(user_id, product_id):
    return Wishlist.objects.filter(user_id=user_id, product_id=product_id).exists()


