from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from products.models import Product
from .models import Cart 

def add_to_cart(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            product_id = request.POST.get('product_id')
            quantity = request.POST.get('quantity')  # get the quantity from the form
            try:
                quantity = int(quantity)
                if quantity < 1:
                    quantity = 1
            except (ValueError, TypeError):
                quantity = 1

            try:
                product = Product.objects.get(id=product_id)
                cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)

                if created:
                    cart_item.quantity = quantity  # set to the form quantity
                else:
                    cart_item.quantity += quantity  # increment by form quantity

                cart_item.save()
                messages.success(request, f'{product.name} has been added to your cart ({cart_item.quantity}).')

            except Product.DoesNotExist:
                messages.error(request, 'Product not found.')

        return redirect('show_cart')
    else:
        messages.error(request,'You must login first to access the page')
        return redirect('login')



from django.db.models import Sum

def show_cart(request):
    if request.user.is_authenticated:
        user = request.user
        cart_items = Cart.objects.filter(user=user)

        # Calculate the total price of items in the cart
        total_cart_price = sum(item.total_cost for item in cart_items)

        # Calculate the total quantity of items in the cart
        total_quantity = cart_items.aggregate(total_count=Sum('quantity'))['total_count'] or 0

        # Pass the cart items, total price, and total quantity to the template
        return render(request, 'user/addcart.html', {
            'cart_items': cart_items,
            'total_cart_price': total_cart_price,
            'total_quantity': total_quantity,  # Pass the total quantity to the template
        })
    else:
        messages.error(request,'You must login first to access the page')
        return redirect('login')



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


# Increment the quantity of a product in the cart
def increment_quantity(request, cart_item_id):
    if request.user.is_authenticated:
        try:
            cart_item = Cart.objects.get(id=cart_item_id, user=request.user)
            cart_item.quantity += 1
            cart_item.save()

            # Calculate the total number of items in the cart
            total_quantity = sum(item.quantity for item in Cart.objects.filter(user=request.user))

            # Return the updated quantity and total cost as well as the total cart quantity
            return JsonResponse({
                'success': True,
                'quantity': cart_item.quantity,
                'total_cost': cart_item.total_cost,
                'total_quantity': total_quantity
            })

        except Cart.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Cart item not found.'})
    else:
        messages.error(request,'You must login first to access the page')
        return redirect('login')

# Decrement the quantity of a product in the cart
def decrement_quantity(request, cart_item_id):
    if request.user.is_authenticated:
        try:
            cart_item = Cart.objects.get(id=cart_item_id, user=request.user)
            if cart_item.quantity > 1:  # Prevent quantity from going below 1
                cart_item.quantity -= 1
                cart_item.save()

                # Calculate the total number of items in the cart
                total_quantity = sum(item.quantity for item in Cart.objects.filter(user=request.user))

                # Return the updated quantity and total cost as well as the total cart quantity
                return JsonResponse({
                    'success': True,
                    'quantity': cart_item.quantity,
                    'total_cost': cart_item.total_cost,
                    'total_quantity': total_quantity
                })
            else:
                return JsonResponse({'success': False, 'message': 'Quantity cannot be less than 1.'})

        except Cart.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Cart item not found.'})
    else:
        messages.error(request,'You must login first to access the page')
        return redirect('login')


