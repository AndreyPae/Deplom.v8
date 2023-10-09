from django.contrib.auth import logout
from django.urls import path
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from .views import register, base_view,login_view, logout_view, product_list, add_to_cart, cart, checkout, product_create, product_detail, product_update, product_delete, category_list, category_create, category_detail, category_update, category_delete, order_list, order_detail, cart_detail, cart_add, cart_update, cart_delete, user_orders

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout_view/', logout_view, name='logout_view'),
    path('product_list/', product_list, name='product_list'),
    path('', base_view, name='base'),
    path('checkout/', checkout, name='checkout'),

    # <--- Создание и редактирование продукта --->

    path('create/', product_create, name='product_create'),
    path('<int:product_id>/', product_detail, name='product_detail'),
    path('<int:product_id>/update/', product_update, name='product_update'),
    path('<int:product_id>/delete/', product_delete, name='product_delete'),
    path('<slug:category_slug>/', product_list, name='product_list_by_category'),
    path('<slug:tag_slug>/', product_list, name='product_list_by_tag'),

    # <--- Создание и редактирование категорий --->

    path('categories/', category_list, name='category_list'),
    path('categories/create/', category_create, name='category_create'),
    path('categories/<int:category_id>/', category_detail, name='category_detail'),
    path('categories/<int:category_id>/update/', category_update, name='category_update'),
    path('categories/<int:category_id>/delete/', category_delete, name='category_delete'),

    # <--- Заказы --->

    path('orders/', order_list, name='order_list'),
    path('my-orders/', user_orders, name='my_orders'),
    path('orders/<int:order_id>/', order_detail, name='order_detail'),

    # <--- Корзина --->

    path('cart/', cart, name='cart'),
    path('add_to_cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/add/<int:product_id>/', cart_add, name='cart_add'),
    path('cart/update/<int:cart_item_id>/', cart_update, name='cart_update'),
    path('cart/delete/<int:cart_item_id>/', cart_delete, name='cart_delete'),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)