# views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import Product, Category, RoofingSheetAttribute, TileAttribute

from django.shortcuts import render
from .models import Product, Category, RoofingSheetAttribute, TileAttribute, ProductGauge

def products(request):
    categories = Category.objects.all()
    products = Product.objects.all()

    # Filtering
    category_id = request.GET.get('category')
    color = request.GET.get('color')
    profile = request.GET.get('profile')
    gauge = request.GET.get('gauge')

    # Filter by category
    if category_id:
        products = products.filter(category_id=category_id)
        category = Category.objects.get(id=category_id)

        if category.name.lower() == "roofing sheet":
            if color:
                products = products.filter(roofing_attributes__color=color)
            if profile:
                products = products.filter(roofing_attributes__profile=profile)
            if gauge:
                products = products.filter(gauges__gauge=gauge)

            colors = RoofingSheetAttribute.objects.filter(product__category=category).values_list('color', flat=True).distinct()
            profiles = RoofingSheetAttribute.objects.filter(product__category=category).values_list('profile', flat=True).distinct()
            gauges = ProductGauge.objects.filter(product__category=category).values_list('gauge', flat=True).distinct()

        elif category.name.lower() == "tiles":
            if color:
                products = products.filter(tile_attributes__color=color)
            if profile:
                products = products.filter(tile_attributes__profile=profile)

            colors = TileAttribute.objects.filter(product__category=category).values_list('color', flat=True).distinct()
            profiles = TileAttribute.objects.filter(product__category=category).values_list('profile', flat=True).distinct()
            gauges = []  # Tiles don’t have gauges

        else:
            colors = []
            profiles = []
            gauges = []

    else:
        colors = []
        profiles = []
        gauges = []

    # ✅ Calculate discount percentage for each product
    for product in products:
        if product.discount_price and product.selling_price:
            product.discount_percentage = round(
                (product.selling_price - product.discount_price) / product.selling_price * 100
            )
        else:
            product.discount_percentage = 0

    context = {
        'categories': categories,
        'products': products,
        'colors': colors,
        'profiles': profiles,
        'gauges': gauges,
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

from django.shortcuts import render, get_object_or_404
from .models import Product, Category

from django.shortcuts import render, get_object_or_404
from .models import Product, Category, RoofingSheetAttribute, TileAttribute, ProductGauge

def category(request, pk):
    # get the category (you use name in URL)
    category_obj = get_object_or_404(Category, name=pk)

    # all categories for sidebar (template expects this)
    categories = Category.objects.all()

    # base queryset: products belonging to this category
    products_qs = Product.objects.filter(category=category_obj)

    # define which category names should be treated as roofing / tiles
    roofing_categories = { 'ando mobile steel structures', 'ando long', 'ando eco', 'roofing sheet' }
    tile_categories = { 'zebra roofing tiles', 'ando decorative wall coatings', 'tiles' }

    # normalize name for matching
    cat_name = (category_obj.name or '').strip().lower()

    # defaults
    colors = []
    profiles = []
    gauges = []

    # If roofing category -> gather attributes from RoofingSheetAttribute and ProductGauge
    if cat_name in roofing_categories:
        # attributes come from the related models
        colors = list(
            RoofingSheetAttribute.objects
            .filter(product__category=category_obj)
            .values_list('color', flat=True)
            .distinct()
        )
        profiles = list(
            RoofingSheetAttribute.objects
            .filter(product__category=category_obj)
            .values_list('profile', flat=True)
            .distinct()
        )
        gauges = list(
            ProductGauge.objects
            .filter(product__category=category_obj)
            .values_list('gauge', flat=True)
            .distinct()
        )

        # apply querystring filters (use related lookups)
        color_filter = request.GET.get('color')
        profile_filter = request.GET.get('profile')
        gauge_filter = request.GET.get('gauge')

        if color_filter:
            products_qs = products_qs.filter(roofing_attributes__color=color_filter)
        if profile_filter:
            products_qs = products_qs.filter(roofing_attributes__profile=profile_filter)
        if gauge_filter:
            products_qs = products_qs.filter(gauges__gauge=gauge_filter)

    # If tile category -> gather attributes from TileAttribute
    elif cat_name in tile_categories:
        colors = list(
            TileAttribute.objects
            .filter(product__category=category_obj)
            .values_list('color', flat=True)
            .distinct()
        )
        profiles = list(
            TileAttribute.objects
            .filter(product__category=category_obj)
            .values_list('profile', flat=True)
            .distinct()
        )
        gauges = []  # tiles typically have no gauges in your models

        # apply querystring filters using tile_attributes lookups
        color_filter = request.GET.get('color')
        profile_filter = request.GET.get('profile')

        if color_filter:
            products_qs = products_qs.filter(tile_attributes__color=color_filter)
        if profile_filter:
            products_qs = products_qs.filter(tile_attributes__profile=profile_filter)

    else:
        # For other categories (e.g., steel, accessories...) try to support steel attributes if present
        # If you have MobileSteelAttribute (steel_attributes) we can add logic here.
        # For now, no attribute filters:
        colors = []
        profiles = []
        gauges = []

    # Recompute products list after filters
    products = products_qs.select_related('category').prefetch_related('gauges', 'roofing_attributes', 'tile_attributes')

    # Add discount_percentage attribute for template (so template arithmetic is avoided)
    for p in products:
        try:
            sp = float(p.selling_price or 0)
            dp = float(p.discount_price or 0)
            if sp and dp and sp > dp:
                p.discount_percentage = round((sp - dp) / sp * 100)
            else:
                p.discount_percentage = 0
        except Exception:
            p.discount_percentage = 0

    context = {
        'products': products,
        'category_name': category_obj.name,
        'categories': categories,
        'colors': colors,
        'profiles': profiles,
        'gauges': gauges,
    }
    return render(request, 'user/category.html', context)
