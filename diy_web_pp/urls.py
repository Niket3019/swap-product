from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('add/', views.add, name='add'),
    path('cart/', views.cart, name='cart'),
    path('contact/', views.contact, name='contact'),
    path('design-studio/', views.design_studio, name='design_studio'),
    path('login/', views.login_view, name='login'),
    path('login_user/', views.login_user, name='login_user'),
    path('second-shop/', views.second_shop, name='second_shop'),
    path('sell-clothes/', views.sell_clothes, name='sell_clothes'),
    path('shop/', views.shop, name='shop'),
    path('sproduct/', views.sproduct, name='sproduct'),
    path('swap-items/', views.swap_items, name='swap-items'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/<int:item_id>/', views.update_cart_quantity, name='update_cart_quantity'),
    path('remove-cart/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('success/<int:order_id>/', views.order_success_view, name='order_success'),
    path('register_user/', views.register_user, name='register_user'),
    path('desing_studio/', views.desing_studio, name='desing_studio'),
    path('logout/', views.logout_view, name='logout'),
    path('my_orders/', views.my_orders, name='my_orders'),
    path('swap/', views.swap_item, name='swap_item'),
    path('explore/', views.browse_items, name='browse_items'),
    path('swap-request/<int:item_id>/', views.send_swap_request, name='send_swap_request'),
    path('chat/<int:swap_id>/', views.chat_view, name='chat_view'),
    path('swap_notification/', views.swap_notification, name='swap_notification'),
    path('accept_swap/', views.accept_swap, name='accept_swap'),
    path('swap_chat/', views.swap_requests_view, name='swap_chat'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

