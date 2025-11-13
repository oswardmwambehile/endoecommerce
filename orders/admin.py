from django.contrib import admin
from django.utils.html import format_html
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # Columns to display in admin list view
    list_display = (
        'id',
        'user_full_name',
        'contact_display',
        'fund_available_display',
        'pickup_location_display',
        'site_region_display',
        'site_location_display',
        'product',
        'category_display',
        'color_display',
        'gauge_display',
        'profile_display',
        'quantity',
        'total_cost_display',
        'status_badge',
        'order_date',
        'updated_at',
    )

    # Filters on sidebar
    list_filter = ('status', 'order_date')

    # Search functionality
    search_fields = (
        'user__first_name',
        'user__last_name',
        'user__email',
        'product__name',
        'user__contact',
    )

    # Default ordering (latest first)
    ordering = ('-order_date',)

    # Paginate results (10 per page)
    list_per_page = 10

    # Read-only fields for system-managed dates
    readonly_fields = ('order_date', 'updated_at')

    # Custom display for user full name
    def user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.email
    user_full_name.short_description = "Customer"

    # New: Contact and extra user info
    def contact_display(self, obj):
        return getattr(obj.user, 'contact', '-')
    contact_display.short_description = "Contact"

    # ✅ Fixed: Show badge for Fund Available (Yes / No)
    def fund_available_display(self, obj):
        value = str(getattr(obj.user, 'fund_available', '-')).strip().lower()
        if value == 'yes':
            return format_html(
                '<span style="background-color:#28a745;color:white;padding:3px 8px;border-radius:8px;">Yes</span>'
            )
        elif value == 'no':
            return format_html(
                '<span style="background-color:#dc3545;color:white;padding:3px 8px;border-radius:8px;">No</span>'
            )
        return "-"
    fund_available_display.short_description = "Fund Available"

    def pickup_location_display(self, obj):
        return getattr(obj.user, 'pickup_location', '-')
    pickup_location_display.short_description = "Pickup Location"

    def site_region_display(self, obj):
        return getattr(obj.user, 'site_region', '-')
    site_region_display.short_description = "Site Region"

    def site_location_display(self, obj):
        return getattr(obj.user, 'site_location', '-')
    site_location_display.short_description = "Site Location"

    # Category name display
    def category_display(self, obj):
        return obj.product.category.name if obj.product and obj.product.category else "-"
    category_display.short_description = "Category"

    # Attribute displays depending on product category
    def color_display(self, obj):
        product = obj.product
        color = "-"
        if hasattr(product, 'roofing_attributes'):
            color = product.roofing_attributes.color
        elif hasattr(product, 'tile_attributes'):
            color = product.tile_attributes.color

        if color != "-":
            return format_html(
                '<span style="display:inline-block; width:15px; height:15px; border-radius:3px; '
                'background-color:{}; margin-right:5px; border:1px solid #ccc;"></span>{}',
                color, color.capitalize()
            )
        return "-"
    color_display.short_description = "Color"

    def gauge_display(self, obj):
        product = obj.product
        if hasattr(product, 'roofing_attributes'):
            return product.roofing_attributes.gauge
        elif hasattr(product, 'tile_attributes'):
            return product.tile_attributes.gauge
        return "-"
    gauge_display.short_description = "Gauge"

    def profile_display(self, obj):
        product = obj.product
        if hasattr(product, 'roofing_attributes'):
            return product.roofing_attributes.profile.capitalize()
        elif hasattr(product, 'tile_attributes'):
            return product.tile_attributes.profile.capitalize()
        return "-"
    profile_display.short_description = "Profile"

    # Custom formatted total cost
    def total_cost_display(self, obj):
        return f"{obj.total_cost:,.2f} TZS"
    total_cost_display.short_description = "Total Cost"

    # Colored status badge
    def status_badge(self, obj):
        color_map = {
            'accepted': '#28a745',
            'packed': '#17a2b8',
            'on_the_way': '#ffc107',
            'delivered': '#007bff',
            'cancel': '#dc3545',
            'pending': '#6c757d',
        }
        color = color_map.get(obj.status, '#6c757d')
        return format_html(
            '<span style="color: white; background-color: {}; padding: 3px 8px; border-radius: 5px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = "Status"
