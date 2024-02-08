from django.template import Library

register = Library()


@register.filter("custom_slice", is_safe=True)
def custom_slice_filter(value, arg: str):
    a, b = map(int, arg.split(':'))
    return list(value)[a: b]

