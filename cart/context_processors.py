from django.db.models import Sum
from .models import Cart

def cart_quantity(request):
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        total_quantity = cart_items.aggregate(total_count=Sum('quantity'))['total_count'] or 0
        return {'total_quantity': total_quantity}
    return {'total_quantity': 0}