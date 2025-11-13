# views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import Product, Category, RoofingSheetAttribute, TileAttribute

def products(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    # Handle filtering
    category_id = request.GET.get('category')
    color = request.GET.get('color')
    gauge = request.GET.get('gauge')
    profile = request.GET.get('profile')

    if category_id:
        products = products.filter(category_id=category_id)
        category = Category.objects.get(id=category_id)
        
        # Apply attribute filters
        if category.name.lower() == 'roofing sheet':
            if color:
                products = products.filter(roofing_attributes__color=color)
            if gauge:
                products = products.filter(roofing_attributes__gauge=gauge)
            if profile:
                products = products.filter(roofing_attributes__profile=profile)

        elif category.name.lower() == 'tiles':
            if color:
                products = products.filter(tile_attributes__color=color)
            if gauge:
                products = products.filter(tile_attributes__gauge=gauge)
            if profile:
                products = products.filter(tile_attributes__profile=profile)

    context = {
        'categories': categories,
        'products': products,
    }
    return render(request, 'user/products.html', context)


def get_attributes(request):
    """AJAX endpoint to fetch available color/gauge/profile for selected category."""
    category_id = request.GET.get('category_id')
    attributes = {}

    if category_id:
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return JsonResponse(attributes)

        if category.name.lower() == 'roofing sheet':
            attrs = RoofingSheetAttribute.objects.filter(product__category=category)
            colors = attrs.values_list('color', flat=True).distinct()
            gauges = attrs.values_list('gauge', flat=True).distinct()
            profiles = attrs.values_list('profile', flat=True).distinct()
            attributes = {
                'colors': list(colors),
                'gauges': list(gauges),
                'profiles': list(profiles),
            }

        elif category.name.lower() == 'tiles':
            attrs = TileAttribute.objects.filter(product__category=category)
            colors = attrs.values_list('color', flat=True).distinct()
            gauges = attrs.values_list('gauge', flat=True).distinct()
            profiles = attrs.values_list('profile', flat=True).distinct()
            attributes = {
                'colors': list(colors),
                'gauges': list(gauges),
                'profiles': list(profiles),
            }

    return JsonResponse(attributes)


from django.shortcuts import render, get_object_or_404
from .models import Product, RoofingSheetAttribute, TileAttribute

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    roofing_attr = getattr(product, 'roofing_attributes', None)
    tile_attr = getattr(product, 'tile_attributes', None)

    # If both exist, decide based on category
    if product.category == 'roofing_sheet':
        roofing_attr = getattr(product, 'roofing_attributes', None)
        tile_attr = None
    elif product.category == 'tiles':
        tile_attr = getattr(product, 'tile_attributes', None)
        roofing_attr = None

    context = {
        'product': product,
        'roofing_attr': roofing_attr,
        'tile_attr': tile_attr,
    }
    return render(request, 'user/product_detail.html', context)



from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product, Category

def category(request, pk):
    if not request.user.is_authenticated:
        messages.error(request, 'You must login first to access the page')
        return redirect('login')
    
    # Use get_object_or_404 with name instead of pk
    category_obj = get_object_or_404(Category, name=pk)
    
    products = Product.objects.filter(category=category_obj)
    
    context = {
        'products': products,
        'category_name': category_obj.name,
    }
    return render(request, 'user/category.html', context)


