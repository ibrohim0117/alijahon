from django.urls import path

from apps.views import (MainTemplateView, ProfileTemplateView,
                        SettingsTemplateView, ProductListView,
                        ProductDetailView, RegisterCreateView,
                        LoginTemplateView, ConfirmMailTemplateView,
                        ForgetPasswordTemplateView, LockScreenTemplateView,
                        LogoutTemplateView, ResetPasswordTemplateView)

urlpatterns = [
    path('main', MainTemplateView.as_view(), name='main'),
    path('profile', ProfileTemplateView.as_view(), name='profile'),
    path('settings', SettingsTemplateView.as_view(), name='settings'),
    path('', ProductListView.as_view(), name='products'),
    path('productdetail/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),

    path('register', RegisterCreateView.as_view(), name='register'),
    path('login', LoginTemplateView.as_view(), name='login'),
    path('confirm_mail', ConfirmMailTemplateView.as_view(), name='confirm_mail'),
    path('forget_password', ForgetPasswordTemplateView.as_view(), name='forget_password'),
    path('lockscreen', LockScreenTemplateView.as_view(), name='lockscreen'),
    path('logout', LogoutTemplateView.as_view(), name='logout'),
    path('reset_password', ResetPasswordTemplateView.as_view(), name='logout'),
]


