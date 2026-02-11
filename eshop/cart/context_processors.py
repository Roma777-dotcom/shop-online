def cart(request):
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())
    cart_total = 0
    
    return {
        'cart_count': cart_count,
        'cart': cart,
    }