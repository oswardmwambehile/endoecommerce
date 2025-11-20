from django.contrib import admin
from django.utils.html import format_html
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user_full_name',
        'contact_display',
        'fund_available_display',
        'pickup_location_display',
        'site_region_display',
        'site_location_display',
        'product',
        'attributes_display',
        'quantity',
        'total_cost_display',
        'status_badge',
        'order_date',
        'updated_at',
    )

    list_filter = ('status', 'order_date')
    search_fields = (
        'user__first_name',
        'user__last_name',
        'user__email',
        'product__name',
        'user__contact',
    )
    ordering = ('-order_date',)
    list_per_page = 10
    readonly_fields = ('order_date', 'updated_at')

    def user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.email
    user_full_name.short_description = "Customer"

    def contact_display(self, obj):
        return getattr(obj.user, 'contact', '-')
    contact_display.short_description = "Contact"

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

    # ---------------- Attributes Display ----------------
    def attributes_display(self, obj):
            attrs = []

            if obj.color:
                attrs.append(f"Color: {obj.color.title()}")
            if obj.profile:
                attrs.append(f"Profile: {obj.profile.title()}")
            if obj.gauge:
                attrs.append(f"Gauge: {obj.gauge.gauge}")
            if obj.length:
                attrs.append(f"Length: {obj.length} m")
            if obj.width:
                attrs.append(f"Width: {obj.width} m")
            if obj.height:
                attrs.append(f"Height: {obj.height} m")

            return format_html("<br>".join(attrs)) if attrs else "—"

    def total_cost_display(self, obj):
        quantity = obj.quantity or 1
        price = obj.price_at_addition or obj.product.selling_price

        if obj.gauge and obj.length:
            total = price * obj.length * quantity
        elif getattr(obj.product, 'steel_attributes', None) and obj.length and obj.width and obj.height:
            total = obj.product.steel_attributes.unit_price * obj.length * obj.width * obj.height * quantity
        else:
            total = price * quantity

        return f"{total:,.2f} TZS"


    # ---------------- Status Badge ----------------
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
            '<span style="color:white; background-color:{}; padding:3px 8px; border-radius:5px;">{}</span>',
            color,
            obj.get_status_display()
        )
    status_badge.short_description = "Status"
