from django.contrib import admin

from .models import Category # Категории
from .models import Product # Продукты
from .models import Order # Заказы
from .models import OrderItem # Предметы в заказе
from .models import Tag # Теги
# from .models import Cart # Корзина
from .models import CartItem # Предметы в корзине

admin.site.register(Category)

admin.site.register(Product)

admin.site.register(Order)
admin.site.register(OrderItem)

admin.site.register(Tag)

# admin.site.register(Cart)
admin.site.register(CartItem)