from django.contrib import admin
from django.utils.translation import gettext_lazy as _


class PriceRangeFilter(admin.SimpleListFilter):
    title = _('Цена')
    parameter_name = 'price'
    
    def lookups(self, request, model_admin):
        return (
            ('0-1000', _('до 1000 руб')),
            ('1000-5000', _('1000-5000 руб')),
            ('5000-10000', _('5000-10000 руб')),
            ('10000+', _('более 10000 руб')),
        )
    
    def queryset(self, request, queryset):
        if self.value() == '0-1000':
            return queryset.filter(price__lte=1000)
        if self.value() == '1000-5000':
            return queryset.filter(price__gt=1000, price__lte=5000)
        if self.value() == '5000-10000':
            return queryset.filter(price__gt=5000, price__lte=10000)
        if self.value() == '10000+':
            return queryset.filter(price__gt=10000)
        return queryset


class StockStatusFilter(admin.SimpleListFilter):
    title = _('Наличие')
    parameter_name = 'stock_status'
    
    def lookups(self, request, model_admin):
        return (
            ('in_stock', _('В наличии')),
            ('low_stock', _('Мало на складе')),
            ('out_of_stock', _('Нет в наличии')),
        )
    
    def queryset(self, request, queryset):
        if self.value() == 'in_stock':
            return queryset.filter(stock__gt=10)
        if self.value() == 'low_stock':
            return queryset.filter(stock__gt=0, stock__lte=10)
        if self.value() == 'out_of_stock':
            return queryset.filter(stock=0)
        return queryset