from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class NotLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_anonymous:
            return redirect('products')
        return super().dispatch(request, *args, **kwargs)


class NotOperatorRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated and not request.user.is_operator and not request.user.is_superuser:
            return redirect('products')
        return super().dispatch(request, *args, **kwargs)
