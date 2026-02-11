from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from datetime import timedelta
from orders.models import Order  

@staff_member_required
def admin_dashboard(request):
    thirty_days_ago = timezone.now() - timedelta(days=30)

    paid_orders = Order.objects.filter(paid=True)

    total_revenue = sum(order.get_total_cost() for order in paid_orders)

    recent_orders = paid_orders.filter(created__gte=thirty_days_ago)
    recent_revenue = sum(order.get_total_cost() for order in recent_orders)
    total_orders = paid_orders.count()
    pending_orders = Order.objects.filter(paid=False).count()

    context = {
        'total_revenue': total_revenue,
        'recent_revenue': recent_revenue,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'recent_orders': recent_orders[:5], 
    }
    
    return render(request, 'admin/dashboard.html', context)