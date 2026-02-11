from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from shop.models import Product
from .models import Order, OrderItem, Payment


@login_required
def order_create(request):
    cart = request.session.get('cart', {})
    
    if not cart:
        messages.warning(request, 'Ваша корзина пуста')
        return redirect('cart:cart_detail')
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method', 'card')
        
        order = Order.objects.create(
            user=request.user,
            first_name=request.POST.get('first_name', ''),
            last_name=request.POST.get('last_name', ''),
            email=request.POST.get('email', request.user.email),
            phone=request.POST.get('phone', ''),
            address=request.POST.get('address', ''),
            city=request.POST.get('city', ''),
            postal_code=request.POST.get('postal_code', ''),
            payment_method=payment_method,
        )
        
        for product_id, quantity in cart.items():
            product = Product.objects.get(id=product_id)
            OrderItem.objects.create(
                order=order,
                product=product,
                price=product.price,
                quantity=quantity
            )
        
        # Очищаем корзину
        del request.session['cart']
        request.session.modified = True
        
        # Если выбрана онлайн оплата, перенаправляем на страницу оплаты
        if payment_method in ['card', 'online']:
            # Создаем запись о платеже
            payment = Payment.objects.create(
                order=order,
                amount=order.total_cost,
                payment_method=payment_method,
                status='pending'
            )
            return redirect('orders:payment_process', order_id=order.id)
        else:
            # Для оплаты наличными при получении сразу отмечаем как неоплаченный
            messages.success(request, f'Заказ #{order.id} успешно создан! Оплата при получении.')
            return redirect('orders:order_detail', order_id=order.id)
    
    product_ids = cart.keys()
    products = Product.objects.filter(id__in=product_ids)
    
    cart_items = []
    total_price = 0
    
    for product in products:
        quantity = cart.get(str(product.id), 0)
        if quantity > 0:
            item_total = product.price * quantity
            cart_items.append({
                'product': product,
                'quantity': quantity,
                'total': item_total
            })
            total_price += item_total
    
    user = request.user
    initial_data = {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'phone': user.phone or '',
        'address': user.address or '',
        'city': user.city or '',
        'postal_code': user.postal_code or '',
    }
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'initial_data': initial_data,
        'title': 'Оформление заказа'
    }
    
    return render(request, 'orders/create.html', context)


@login_required
def order_detail(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    
    context = {
        'order': order,
        'title': f'Заказ #{order.id}'
    }
    
    return render(request, 'orders/detail.html', context)


@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created')
    
    context = {
        'orders': orders,
        'title': 'Мои заказы'
    }
    
    return render(request, 'orders/list.html', context)


@login_required
def payment_process(request, order_id):
    """Страница обработки платежа"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.payment_method not in ['card', 'online']:
        messages.warning(request, 'Для этого заказа не требуется онлайн оплата')
        return redirect('orders:order_detail', order_id=order.id)
    
    # Получаем или создаем платеж
    payment, created = Payment.objects.get_or_create(
        order=order,
        defaults={
            'amount': order.total_cost,
            'payment_method': order.payment_method,
            'status': 'pending'
        }
    )
    
    if payment.status == 'completed':
        messages.info(request, 'Этот заказ уже оплачен')
        return redirect('orders:order_detail', order_id=order.id)
    
    context = {
        'order': order,
        'payment': payment,
        'title': f'Оплата заказа #{order.id}'
    }
    
    return render(request, 'orders/payment.html', context)


@login_required
def payment_done(request, order_id):
    """Успешная оплата"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    try:
        payment = Payment.objects.get(order=order)
        payment.status = 'completed'
        payment.transaction_id = f'TXN-{order.id}-{payment.id}'
        payment.save()
        
        order.paid = True
        order.status = 'processing'
        order.save()
        
        messages.success(request, f'Заказ #{order.id} успешно оплачен!')
    except Payment.DoesNotExist:
        messages.error(request, 'Платеж не найден')
    
    return redirect('orders:order_detail', order_id=order.id)


@login_required
def payment_canceled(request, order_id):
    """Отмена оплаты"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    try:
        payment = Payment.objects.get(order=order)
        payment.status = 'failed'
        payment.save()
        
        messages.warning(request, f'Оплата заказа #{order.id} была отменена. Вы можете попробовать оплатить заказ позже.')
    except Payment.DoesNotExist:
        messages.error(request, 'Платеж не найден')
    
    return redirect('orders:order_detail', order_id=order.id)
