from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'status', 'paid']
    
    actions = ['mark_as_paid', 'mark_as_unpaid']
    
    def mark_as_paid(self, request, queryset):
        queryset.update(paid=True)
    mark_as_paid.short_description = "Отметить как оплаченные"
    
    def mark_as_unpaid(self, request, queryset):
        queryset.update(paid=False)
    mark_as_unpaid.short_description = "Отметить как неоплаченные"
