from django.urls import path

from apps.views import (MainTemplateView, ProfileTemplateView,
                        SettingsTemplateView, ProductListView,
                        ProductDetailView, RegisterCreateView,
                        LoginFormView, ConfirmMailTemplateView,
                        ForgetPasswordTemplateView, LockScreenTemplateView,
                        LogoutRedirectView, ResetPasswordTemplateView,
                        WishlistCreateView, ShoppingListView,
                        UpdateViewProfile, OrderSuccessTemplateView,
                        OrderCreateView, OrderListView, OrderUpdateView,
                        OrderREADYTODELIVERYListView, OrderARCHIVEListView,
                        OrderDELIVEREDListView, OrderBROKENListView,
                        OrderRETURNEDListView, OrderCANCELLEDListView,
                        OrderWAITINGListView, MarketListView,
                        StreamFormView, StreamListView,
                        StatistikaListView, MyOrdersListView)


urlpatterns = [
    path('', ProductListView.as_view(), name='products'),
    path('main', MainTemplateView.as_view(), name='main'),
    path('profile/', ProfileTemplateView.as_view(), name='profile'),
    path('update', UpdateViewProfile.as_view(), name='update_profile'),
    path('settings', SettingsTemplateView.as_view(), name='settings'),
    path('shop', ShoppingListView.as_view(), name='shop'),
    path('product/<str:slug>', ProductDetailView.as_view(), name='product_detail'),
    path('stream-list/<int:pk>/', ProductDetailView.as_view(), name='stream_detail'),
    path('liked/<slug:slug>', WishlistCreateView.as_view(), name='wishlist'),
    path('success-product/<int:pk>', OrderSuccessTemplateView.as_view(), name='success_product'),


    path('register', RegisterCreateView.as_view(), name='register'),
    path('login', LoginFormView.as_view(), name='login'),
    path('confirm_mail', ConfirmMailTemplateView.as_view(), name='confirm_mail'),
    path('forget_password', ForgetPasswordTemplateView.as_view(), name='forget_password'),
    path('lockscreen', LockScreenTemplateView.as_view(), name='lockscreen'),
    path('logout', LogoutRedirectView.as_view(), name='logout'),
    path('reset_password', ResetPasswordTemplateView.as_view(), name='reset_password'),
]


# order
urlpatterns += [
    path('order', OrderCreateView.as_view(), name='order'),
    path('my-order', MyOrdersListView.as_view(), name='my_order'),
    path('order-list', OrderListView.as_view(), name='order_list'),
    path('order/<int:pk>/', OrderUpdateView.as_view(), name='order_update'),
    path('yetkazishga-tayyor', OrderREADYTODELIVERYListView.as_view(), name='yetkazishga_tayyor_list'),
    path('arxivlandi', OrderARCHIVEListView.as_view(), name='arxivlandi'),
    path('yetkazildi', OrderDELIVEREDListView.as_view(), name='yetkazildi'),
    path('nosoz-mahsukot', OrderBROKENListView.as_view(), name='nosoz_mahsukot'),
    path('qaytib-keldi', OrderRETURNEDListView.as_view(), name='qaytib_keldi'),
    path('bekor-qilindi', OrderCANCELLEDListView.as_view(), name='bekor_qilindi'),
    path('kiyin-oladi', OrderWAITINGListView.as_view(), name='kiyin_oladi'),


    path('market', MarketListView.as_view(), name='market'),
    path('stream', StreamFormView.as_view(), name='stream'),
    path('stream-list', StreamListView.as_view(), name='stream_list'),
    path('statistika', StatistikaListView.as_view(), name='statistika'),

]


