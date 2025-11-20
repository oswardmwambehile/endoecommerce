from django.contrib import admin
from .models import Cart

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'product', 'color', 'profile', 'gauge',
        'length', 'width', 'height', 'quantity', 'price_at_addition', 'total_cost', 'created_at'
    )
    list_filter = (
        'product', 'user', 'color', 'profile', 'gauge', 'created_at'
    )
    search_fields = (
        'product__name', 'user__username', 'color', 'profile'
    )
    readonly_fields = (
        'price_at_addition', 'total_cost', 'created_at', 'updated_at'
    )
    fieldsets = (
        ('User & Product', {
            'fields': ('user', 'product')
        }),
        ('Roofing / Tiles', {
            'fields': ('color', 'profile', 'gauge', 'length')
        }),
        ('Steel', {
            'fields': ('width', 'height')
        }),
        ('Quantity & Pricing', {
            'fields': ('quantity', 'price_at_addition', 'total_cost')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    ordering = ('-created_at',)
