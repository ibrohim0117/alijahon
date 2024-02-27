from django.urls import path

from apps.views import (MainTemplateView, ProfileTemplateView,
                        SettingsTemplateView, ProductListView,
                        ProductDetailView, RegisterCreateView,
                        LoginFormView, ConfirmMailTemplateView,
                        ForgetPasswordTemplateView, LockScreenTemplateView,
                        LogoutRedirectView, ResetPasswordTemplateView,
                        WishlistCreateView, ShoppingListView,
                        UpdateViewProfile)

urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('main', MainTemplateView.as_view(), name='main'),
    path('profile/', ProfileTemplateView.as_view(), name='profile'),
    path('update/<int:pk>/', UpdateViewProfile.as_view(), name='update_profile'),
    path('settings', SettingsTemplateView.as_view(), name='settings'),
    path('shop', ShoppingListView.as_view(), name='shop'),
    path('product/<slug:slug>', ProductDetailView.as_view(), name='product_detail'),
    path('liked/<slug:slug>', WishlistCreateView.as_view(), name='wishlist'),

    path('register', RegisterCreateView.as_view(), name='register'),
    path('login', LoginFormView.as_view(), name='login'),
    path('confirm_mail', ConfirmMailTemplateView.as_view(), name='confirm_mail'),
    path('forget_password', ForgetPasswordTemplateView.as_view(), name='forget_password'),
    path('lockscreen', LockScreenTemplateView.as_view(), name='lockscreen'),
    path('logout', LogoutRedirectView.as_view(), name='logout'),
    path('reset_password', ResetPasswordTemplateView.as_view(), name='reset_password'),
]


