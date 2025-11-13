from django.contrib import admin
from .models import Cart

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_full_name', 'product', 'quantity', 'total_cost_display', 'created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at', 'user__user_type')
    search_fields = ('user__first_name', 'user__last_name', 'user__email', 'product__name')
    ordering = ('-created_at',)
    list_per_page = 10  # ✅ Pagination of 10 per page

    def user_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.email
    user_full_name.short_description = "Customer"

    def total_cost_display(self, obj):
        return f"{obj.total_cost:,.2f} TZS"
    total_cost_display.short_description = "Total Cost"

    