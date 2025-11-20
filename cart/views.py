from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product
from .models import Cart 

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product, ProductGauge
from .models import Cart

def add_to_cart(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You must login first.')
        return redirect('login')

    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = request.POST.get('quantity', 1)
        gauge_id = request.POST.get('gauge')
        color = request.POST.get('color')
        profile = request.POST.get('profile')

        # Convert numeric fields to float safely
        try:
            length = float(request.POST.get('length')) if request.POST.get('length') else None
        except ValueError:
            length = None
        try:
            width = float(request.POST.get('width')) if request.POST.get('width') else None
        except ValueError:
            width = None
        try:
            height = float(request.POST.get('height')) if request.POST.get('height') else None
        except ValueError:
            height = None

        try:
            quantity = max(1, int(quantity))
        except (ValueError, TypeError):
            quantity = 1

        # Get product and gauge
        product = get_object_or_404(Product, id=product_id)
        gauge = ProductGauge.objects.filter(id=gauge_id).first() if gauge_id else None

        # Determine cart filter conditions
        cart_filters = {
            'user': request.user,
            'product': product,
            'gauge': gauge,
            'color': color,
            'profile': profile
        }

        cart_defaults = {
            'quantity': quantity,
            'length': length,
            'width': width,
            'height': height
        }

        # Get or create cart item
        cart_item, created = Cart.objects.get_or_create(
            **cart_filters,
            defaults=cart_defaults
        )

        if not created:
            # Update existing cart item
            cart_item.quantity += quantity
            cart_item.length = length or cart_item.length
            cart_item.width = width or cart_item.width
            cart_item.height = height or cart_item.height
            cart_item.save()
        else:
            cart_item.save()  # triggers price_at_addition

        # Success message
        desc = product.name
        if color:
            desc += f" - {color}"
        if profile:
            desc += f" / {profile}"
        if gauge:
            desc += f" (Gauge: {gauge.gauge})"

        messages.success(
            request,
            f"{desc} added to cart. Quantity: {cart_item.quantity}. Total Cost: {cart_item.total_cost:,.0f} TZS"
        )
        return redirect('product_detail', pk=product.id)

    return redirect('product_lists')




from django.db.models import Sum

from django.shortcuts import render, redirect
from django.contrib import messages
from django.db.models import Sum
from .models import Cart

def show_cart(request):
    if not request.user.is_authenticated:
        messages.error(request, 'You must login first.')
        return redirect('login')

    cart_items = Cart.objects.filter(user=request.user)
    total_cart_price = sum(item.total_cost for item in cart_items)
    total_quantity = cart_items.aggregate(total_count=Sum('quantity'))['total_count'] or 0

    return render(request, 'user/addcart.html', {
        'cart_items': cart_items,
        'total_cart_price': total_cart_price,
        'total_quantity': total_quantity,
    })


def remove_from_cart(request, cart_item_id):
    if request.user.is_authenticated:
        try:
            # Get the cart item based on the provided cart_item_id and the logged-in user
            cart_item = Cart.objects.get(id=cart_item_id, user=request.user)
            
            # Remove the cart item
            cart_item.delete()

            messages.success(request, f'{cart_item.product.name} has been removed from your cart.')

        except Cart.DoesNotExist:
            messages.error(request, 'The product was not found in your cart.')

        # Redirect back to the cart page after removing the product
        return redirect('show_cart')  # Ensure 'show_cart' is the name of the cart page view
    else:
        messages.error(request,'You must login first to access the page')
        return redirect('login')
 


from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib import messages

def increment_quantity(request, cart_item_id):
    if request.user.is_authenticated:
        try:
            cart_item = Cart.objects.get(id=cart_item_id, user=request.user)
            cart_item.quantity += 1
            cart_item.save()

            # Calculate totals
            total_quantity = sum(item.quantity for item in Cart.objects.filter(user=request.user))
            total_cart_price = sum(item.total_cost for item in Cart.objects.filter(user=request.user))

            # Return JSON with everything needed for dynamic updates
            return JsonResponse({
                'success': True,
                'quantity': cart_item.quantity,
                'total_cost': cart_item.total_cost,
                'total_cart_price': total_cart_price,
                'total_quantity': total_quantity
            })

        except Cart.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Cart item not found.'})
    else:
        messages.error(request,'You must login first to access the page')
        return redirect('login')


def decrement_quantity(request, cart_item_id):
    if request.user.is_authenticated:
        try:
            cart_item = Cart.objects.get(id=cart_item_id, user=request.user)
            if cart_item.quantity > 1:  # Prevent quantity from going below 1
                cart_item.quantity -= 1
                cart_item.save()

                # Calculate totals
                total_quantity = sum(item.quantity for item in Cart.objects.filter(user=request.user))
                total_cart_price = sum(item.total_cost for item in Cart.objects.filter(user=request.user))

                return JsonResponse({
                    'success': True,
                    'quantity': cart_item.quantity,
                    'total_cost': cart_item.total_cost,
                    'total_cart_price': total_cart_price,
                    'total_quantity': total_quantity
                })
            else:
                return JsonResponse({'success': False, 'message': 'Quantity cannot be less than 1.'})

        except Cart.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Cart item not found.'})
    else:
        messages.error(request,'You must login first to access the page')
        return redirect('login')
