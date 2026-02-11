from django.contrib import admin
from .models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'stock', 'available']
    
    actions = ['make_available', 'make_unavailable']
    
    def make_available(self, request, queryset):
        queryset.update(available=True)
    make_available.short_description = "Сделать доступными"
    
    def make_unavailable(self, request, queryset):
        queryset.update(available=False)
    make_unavailable.short_description = "Сделать недоступными"


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    actions = []  