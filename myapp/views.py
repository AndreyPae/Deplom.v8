from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from django.db.models import Q, Sum

from .models import Product, CartItem, Order, OrderItem, Category, Tag

from .forms import ProductForm, CategoryForm, CartItemForm, OrderForm
from .forms import CustomUserCreationForm


@user_passes_test(lambda u: u.is_superuser)
def admin_view(request):
    # код представления для администраторов
    return render(request, 'admin/admin_view.html')

# <--- Регистрация --->


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login_view(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def base_view(request):
    print(request.user.is_authenticated)
    return render(request, 'base.html', {"user": request.user})


# <--- Авторизация --->


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user

                  )
            return redirect('base')
    return render(request, 'registration/login.html')

# <--- Выход --->


def logout_view(request):
    logout(request)
    return redirect('base')


# <--- Список продуктов --->


@login_required
def product_list(request, category_slug=None):
    print(category_slug)
    query = request.GET.get('q')
    categories = request.GET.get('categories')
    tag = request.GET.get('tag')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    available = bool(request.GET.get('available'))

    products = Product.objects.all()

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    if categories:
        products = products.filter(category__name=categories)

    if tag:
        products = products.filter(tags__name=tag)

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    if available:
        products = products.filter(available=available)

    categories = Category.objects.all()
    tags = Tag.objects.all()

    context = {
        'products': products,
        'categories': categories,
        'tags': tags,
        'query': query,
        'categories': categories,
        'tag': tag,
        'min_price': min_price,
        'max_price': max_price,
        'available': available,
    }

    return render(request, 'product/product_list.html', context)

# <--- Создание продукта --->


@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            return redirect('product_detail', product.id)
    else:
        form = ProductForm()
    return render(request, 'product/product_form.html', {'form': form})

# <--- Описание продукта --->


@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'product/product_detail.html', {'product': product})

# <--- Редактирование продукта --->


@login_required
def product_update(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', product.id)
    else:
        form = ProductForm(instance=product)
    return render(request, 'product/product_form.html', {'form': form})

# <--- Удаление продукта --->


@login_required
def product_delete(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('product_list')

# <--- Список категорий --->


@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category/category_list.html', {'categories': categories})

# <--- Создание категории --->


@login_required
def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            return redirect('category_detail', category.id)
    else:
        form = CategoryForm()
    return render(request, 'category/category_form.html', {'form': form})

# <--- Информация категории --->


@login_required
def category_detail(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    return render(request, 'category/category_detail.html', {'category': category})

# <--- Изменение категории --->


@login_required
def category_update(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_detail', category.id)
    else:
        form = CategoryForm(instance=category)
    return render(request, 'category/category_form.html', {'form': form})

# <--- Удаление категории --->


@login_required
def category_delete(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect('category_list')

# <--- Список заказов --->


@login_required
def order_list(request):
    orders = Order.objects.all()
    context = {
        'orders': orders,
    }
    return render(request, 'order/order_list.html', context)

# <--- Детали заказа --->


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order/order_detail.html', {'order': order})

# <--- Добавление в корзину --->


@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    if request.method == 'POST':
        form = CartItemForm(request.POST)
        if form.is_valid():
            # quantity = form.cleaned_data['quantity']
            # options = form.cleaned_data['options']
            # # cart = Cart.objects.get(user=request.user)  # Получаем текущую корзину пользователя
            # cart_item = CartItem(user=request.user, product=product, quantity=quantity, options=options, cart=cart)
            # cart_item.save()
            return redirect('cart')
    else:
        form = CartItemForm()
    return render(request, 'cart/add_to_cart.html', {'product': product, 'form': form})
# <--- Изменения в корзине --->


@login_required
def remove_from_cart(request, cart_item_id):
    cart_item = CartItem.objects.get(id=cart_item_id)
    if cart_item.user == request.user:
        cart_item.delete()
    return redirect('cart')

# <--- Корзина --->


@login_required
def cart(request):
    try:
        user = request.user
        cart_items = CartItem.objects.filter(user=user).all()
        return render(request, 'cart/cart.html', {'cart_items': cart_items})
    except CartItem.DoesNotExist:
        # Обработка случая, когда корзина не найдена
        return render(request, 'cart/empty_cart.html')

# <--- Информация об корзине --->


@login_required
def cart_detail(request):
    cart_items = CartItem.objects.filter(user=request.user)
    return render(request, 'cart/cart_detail.html', {'cart_items': cart_items})

# <--- Добавление в корзину --->


@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart_detail')

# <--- Изменения в корзине --->


@login_required
def cart_update(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    if request.method == 'POST':
        form = CartItemForm(request.POST, instance=cart_item)
        if form.is_valid():
            form.save()
            return redirect('cart_detail')
    else:
        form = CartItemForm(instance=cart_item)
    return render(request, 'cart/cart_update.html', {'form': form})

# <--- Удаление из корзины --->


@login_required
def cart_delete(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id, user=request.user)
    cart_item.delete()
    return redirect('cart_detail')

# <--- Проверка предметов в корзине  --->


@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for cart_item in cart_items:
                order.items.add(cart_item)
            cart_items.delete()
            return redirect('order/order_confirmation', order_id=order.id)
    else:
        form = OrderForm()
    return render(request, 'checkout.html', {'cart_items': cart_items, 'form': form})

# <--- Заказы пользователя --->


@login_required
def user_orders(request):
    user_email = request.user.email
    orders = Order.objects.filter(customer_email=user_email)
    context = {
        'orders': orders,
    }
    return render(request, 'user/user_orders.html', context)

# <--- Подтверждение заказа --->


@login_required
def order_confirmation(request):
    order = Order.objects.get()
    total_price = order.items.all().aggregate(Sum('product__price')).get('product__price__sum')

    context = {
        'order': order,
        'total_price': total_price
    }

    return render(request, 'order_confirmation.html', context)
