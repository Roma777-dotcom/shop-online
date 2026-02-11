from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['product_link', 'quantity', 'unit_price', 'total_price']
    fields = ['product_link', 'quantity', 'unit_price', 'total_price']
    
    def product_link(self, obj):
        if obj.product:
            url = reverse('admin:shop_product_change', args=[obj.product.id])
            return format_html('<a href="{}">{}</a>', url, obj.product.name)
        return "Товар не найден"
    product_link.short_description = 'Товар'
    
    def unit_price(self, obj):
        return f"{obj.product.price} ₽"
    unit_price.short_description = 'Цена за единицу'
    
    def total_price(self, obj):
        return f"{obj.product.price * obj.quantity} ₽"
    total_price.short_description = 'Общая стоимость'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_link', 'items_count', 'total_price', 'created', 'updated']
    list_filter = ['created', 'updated']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ['created', 'updated', 'cart_summary']
    inlines = [CartItemInline]
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('user', 'session_key')
        }),
        ('Содержимое корзины', {
            'fields': ('cart_summary',)
        }),
        ('Даты', {
            'fields': ('created', 'updated')
        }),
    )
    
    def user_link(self, obj):
        if obj.user:
            url = reverse('admin:accounts_user_change', args=[obj.user.id])
            return format_html('<a href="{}">{}</a>', url, obj.user.email)
        return "Анонимный пользователь"
    user_link.short_description = 'Пользователь'
    
    def items_count(self, obj):
        return obj.items.count()
    items_count.short_description = 'Товаров'
    
    def total_price(self, obj):
        total = sum(item.product.price * item.quantity for item in obj.items.all())
        return f"{total} ₽"
    total_price.short_description = 'Общая сумма'
    
    def cart_summary(self, obj):
        items = obj.items.all()
        if not items:
            return "Корзина пуста"
        
        html = '<table class="table table-sm">'
        html += '<thead><tr><th>Товар</th><th>Цена</th><th>Кол-во</th><th>Итого</th></tr></thead>'
        html += '<tbody>'
        
        total = 0
        for item in items:
            item_total = item.product.price * item.quantity
            total += item_total
            
            html += f'<tr>'
            html += f'<td>{item.product.name}</td>'
            html += f'<td>{item.product.price} ₽</td>'
            html += f'<td>{item.quantity}</td>'
            html += f'<td>{item_total} ₽</td>'
            html += f'</tr>'
        
        html += f'<tr><td colspan="3"><strong>Общая сумма:</strong></td><td><strong>{total} ₽</strong></td></tr>'
        html += '</tbody></table>'
        
        return format_html(html)
    cart_summary.short_description = 'Содержимое корзины'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'cart_link', 'product_link', 'quantity', 'unit_price', 'total_price']
    list_filter = ['cart__created']
    search_fields = ['product__name', 'cart__user__email']
    
    def cart_link(self, obj):
        url = reverse('admin:cart_cart_change', args=[obj.cart.id])
        return format_html('<a href="{}">Корзина #{}</a>', url, obj.cart.id)
    cart_link.short_description = 'Корзина'
    
    def product_link(self, obj):
        url = reverse('admin:shop_product_change', args=[obj.product.id])
        return format_html('<a href="{}">{}</a>', url, obj.product.name)
    product_link.short_description = 'Товар'
    
    def unit_price(self, obj):
        return f"{obj.product.price} ₽"
    unit_price.short_description = 'Цена за единицу'
    
    def total_price(self, obj):
        return f"{obj.product.price * obj.quantity} ₽"
    total_price.short_description = 'Общая стоимость'
