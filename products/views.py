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

        # Define your categories exactly
        roofing_categories = [
            'ando mobile steel structures', 
            'ando long', 
            'ando eco'
        ]
        tile_categories = [
            'zebra roofing tiles', 
            'ando decorative wall coatings'
        ]

        # Apply attribute filterszz
        if category.name.lower() in roofing_categories:
            if color:
                products = products.filter(roofing_attributes__color=color)
            if gauge:
                products = products.filter(roofing_attributes__gauge=gauge)
            if profile:
                products = products.filter(roofing_attributes__profile=profile)

        elif category.name.lower() in tile_categories:
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
    attributes = {'colors': [], 'gauges': [], 'profiles': []}

    if not category_id:
        return JsonResponse(attributes)

    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return JsonResponse(attributes)

    # Define your categories exactly
    roofing_categories = [
        'ando mobile steel structures', 
        'ando long', 
        'ando eco'
    ]
    tile_categories = [
        'zebra roofing tiles', 
        'ando decorative wall coatings'
    ]

    # Collect attributes dynamically
    attrs = []
    if category.name.lower() in roofing_categories:
        attrs = RoofingSheetAttribute.objects.filter(product__category=category)
    elif category.name.lower() in tile_categories:
        attrs = TileAttribute.objects.filter(product__category=category)

    if attrs:
        attributes = {
            'colors': list(attrs.values_list('color', flat=True).distinct()),
            'gauges': list(attrs.values_list('gauge', flat=True).distinct()),
            'profiles': list(attrs.values_list('profile', flat=True).distinct()),
        }

    return JsonResponse(attributes)



from django.shortcuts import render, get_object_or_404
from .models import Product

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)

    roofing_attr = getattr(product, 'roofing_attributes', None)
    tile_attr = getattr(product, 'tile_attributes', None)
    steel_attr = getattr(product, 'steel_attributes', None)

    # Determine dropdown options
    color_choices = []
    profile_choices = []

    if roofing_attr:
        color_choices = roofing_attr.color_choices()
        profile_choices = roofing_attr.profile_choices()
    elif tile_attr:
        color_choices = tile_attr.color_choices()
        profile_choices = tile_attr.profile_choices()

    # Gauges
    gauges = product.gauges.all() if hasattr(product, 'gauges') else []

    # ✔ NEW: Accessories section (NON-destructive)
    accessories_products = Product.objects.filter(
        category__name="Accessories"
    ).exclude(id=product.id)

    context = {
        'product': product,
        'roofing_attr': roofing_attr,
        'tile_attr': tile_attr,
        'steel_attr': steel_attr,
        'color_choices': color_choices,
        'profile_choices': profile_choices,
        'gauges': gauges,
        'accessories_products': accessories_products,   # ← added
    }

    return render(request, 'user/product_detail.html', context)







from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Product, Category

def category(request, pk):
    # Use get_object_or_404 with name instead of pk
    category_obj = get_object_or_404(Category, name=pk)
    
    products = Product.objects.filter(category=category_obj)
    
    context = {
        'products': products,
        'category_name': category_obj.name,
    }
    return render(request, 'user/category.html', context)


