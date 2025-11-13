from django.contrib import admin
from .models import Category, Product, RoofingSheetAttribute, TileAttribute

# Inline for RoofingSheet Attributes
class RoofingSheetAttributeInline(admin.StackedInline):
    model = RoofingSheetAttribute
    extra = 0
    max_num = 1
    fields = ('color', 'gauge', 'profile')
    verbose_name = "Roofing Sheet Attributes"
    verbose_name_plural = "Roofing Sheet Attributes"

# Inline for Tile Attributes
class TileAttributeInline(admin.StackedInline):
    model = TileAttribute
    extra = 0
    max_num = 1
    fields = ('color', 'gauge', 'profile')
    verbose_name = "Tile Attributes"
    verbose_name_plural = "Tile Attributes"


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'selling_price', 'discount_price')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')
    list_per_page = 10  # Pagination: 10 items per page

    inlines = []

    # Show the relevant inline based on category
    def get_inline_instances(self, request, obj=None):
        inlines = []
        if obj:
            cat_name = obj.category.name.lower()
            if cat_name == 'roofing sheet':
                inlines = [RoofingSheetAttributeInline(self.model, self.admin_site)]
            elif cat_name == 'tiles':
                inlines = [TileAttributeInline(self.model, self.admin_site)]
        return inlines


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    list_per_page = 10


@admin.register(RoofingSheetAttribute)
class RoofingSheetAttributeAdmin(admin.ModelAdmin):
    list_display = ('product', 'color', 'gauge', 'profile')
    search_fields = ('product__name',)
    list_filter = ('color', 'gauge', 'profile')
    list_per_page = 10


@admin.register(TileAttribute)
class TileAttributeAdmin(admin.ModelAdmin):
    list_display = ('product', 'color', 'gauge', 'profile')
    search_fields = ('product__name',)
    list_filter = ('color', 'gauge', 'profile')
    list_per_page = 10
