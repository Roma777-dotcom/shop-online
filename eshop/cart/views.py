from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product


def cart_detail(request):
    cart = request.session.get('cart', {})
    
    # Получаем товары из корзины
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
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'title': 'Корзина покупок'
    }
    return render(request, 'cart/detail.html', context)


@require_POST
def cart_add(request, product_id):
    cart = request.session.get('cart', {})
    
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    
    product_key = str(product.id)
    current_quantity = cart.get(product_key, 0)
    cart[product_key] = current_quantity + quantity
    
    request.session['cart'] = cart
    request.session.modified = True
    
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = request.session.get('cart', {})
    
    product_key = str(product_id)
    if product_key in cart:
        del cart[product_key]
        request.session['cart'] = cart
        request.session.modified = True
    
    return redirect('cart:cart_detail')


def cart_update(request, product_id):
    if request.method == 'POST':
        cart = request.session.get('cart', {})
        
        product_key = str(product_id)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0:
            cart[product_key] = quantity
        elif product_key in cart:
            del cart[product_key]
        
        request.session['cart'] = cart
        request.session.modified = True
    
    return redirect('cart:cart_detail')


def cart_clear(request):
    if 'cart' in request.session:
        del request.session['cart']
    
    return redirect('cart:cart_detail')
