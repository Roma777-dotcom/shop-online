from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    
    products = Product.objects.filter(available=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    all_products = Product.objects.all()
    if category_slug:
        all_products = all_products.filter(category=category)
    
    total_products = all_products.count()
    available_count = all_products.filter(available=True).count()
    low_stock_count = all_products.filter(stock__lt=10, stock__gt=0).count()
    out_of_stock_count = all_products.filter(stock=0).count()
    
    context = {
        'category': category,
        'categories': categories,
        'products': products,
        'total_products': total_products,
        'available_count': available_count,
        'low_stock_count': low_stock_count,
        'out_of_stock_count': out_of_stock_count,
        'title': f'Каталог товаров - {category.name if category else "Все товары"}'
    }
    return render(request, 'shop/product/list.html', context)


def product_detail(request, id, slug):
    product = get_object_or_404(
        Product,
        id=id,
        slug=slug,
        available=True
    )
    
    context = {
        'product': product,
        'title': product.name
    }
    return render(request, 'shop/product/detail.html', context)


def category_list(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
        'title': 'Категории товаров'
    }
    return render(request, 'shop/category/list.html', context)


def search(request):
    query = request.GET.get('q', '')
    products = Product.objects.filter(available=True)
    
    if query:
        products = products.filter(name__icontains=query)
    
    context = {
        'products': products,
        'query': query,
        'title': f'Результаты поиска: {query}'
    }
    return render(request, 'shop/product/search.html', context)
