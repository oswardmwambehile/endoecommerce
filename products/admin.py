from django.contrib import admin
from .models import (
    Category,
    Product,
    ProductGauge,
    RoofingSheetAttribute,
    TileAttribute,
    MobileSteelAttribute,
)

# -----------------------------
# Category Admin
# -----------------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)
    list_per_page = 20

# -----------------------------
# ProductGauge Admin
# -----------------------------
@admin.register(ProductGauge)
class ProductGaugeAdmin(admin.ModelAdmin):
    list_display = ('product', 'gauge', 'price_per_meter')
    search_fields = ('product__name', 'gauge')

# -----------------------------
# ProductGauge Inline for Product
# -----------------------------
class ProductGaugeInline(admin.TabularInline):
    model = ProductGauge
    extra = 1
    fields = ('gauge', 'price_per_meter')
    show_change_link = True

# -----------------------------
# Product Admin
# -----------------------------
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'selling_price', 'discount_price')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')
    inlines = [ProductGaugeInline]
    ordering = ('category', 'name')
    list_per_page = 20

# -----------------------------
# RoofingSheetAttribute Admin
# -----------------------------
@admin.register(RoofingSheetAttribute)
class RoofingSheetAttributeAdmin(admin.ModelAdmin):
    list_display = ('product', 'color', 'profile')
    list_filter = ('color', 'profile')
    search_fields = ('product__name',)
    list_per_page = 20

# -----------------------------
# TileAttribute Admin
# -----------------------------
@admin.register(TileAttribute)
class TileAttributeAdmin(admin.ModelAdmin):
    list_display = ('product', 'color', 'profile')
    list_filter = ('color', 'profile')
    search_fields = ('product__name',)
    list_per_page = 20

# -----------------------------
# MobileSteelAttribute Admin
# -----------------------------
@admin.register(MobileSteelAttribute)
class MobileSteelAttributeAdmin(admin.ModelAdmin):
    list_display = ('product', 'unit_price')
    search_fields = ('product__name',)
    list_per_page = 20
