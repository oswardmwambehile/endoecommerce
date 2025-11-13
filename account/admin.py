from django.contrib import admin
from django.utils.html import format_html
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

# 🏗️ Custom admin branding
admin.site.site_header = "🏗️ Roofing Sheet And Tiles E-Commerce"
admin.site.site_title = "Admin Panel"
admin.site.index_title = "Welcome to the Admin Dashboard"


class BaseAdmin(admin.ModelAdmin):
    class Media:
        css = {
            'all': ('account/admin_custom.css',)  # path relative to STATICFILES_DIRS
        }


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Advanced Admin panel for custom User model."""

    # ✅ List view columns
    list_display = (
        'colored_name',
        'email',
        'user_type',
        'fund_badge',
        'pickup_location',
        'site_region',
        'site_location',
        'contact',
        'is_active',
        'is_staff',
        'is_superuser',
        'date_joined',
    )
    list_display_links = ('colored_name', 'email')
    list_editable = ('is_active',)
    list_per_page = 20

    # ✅ Filters and search
    list_filter = (
        'user_type',
        'fund_available',
        'is_active',
        'is_staff',
        'is_superuser',
        'pickup_location',
        'site_region',
    )
    search_fields = (
        'email',
        'first_name',
        'last_name',
        'contact',
        'pickup_location',
        'site_region',
    )
    ordering = ('-date_joined',)  # Default ordering (newest first)

    # ✅ Force queryset to order by latest user
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('-date_joined')  # Ensures latest users appear first

    # ✅ Display all fields nicely grouped
    fieldsets = (
        ("👤 Personal Information", {
            'fields': ('email', 'first_name', 'last_name', 'contact'),
        }),
        ("📍 Location Details", {
            'fields': ('pickup_location', 'site_region', 'site_location'),
        }),
        ("💼 Account Details", {
            'fields': ('user_type', 'fund_available'),
        }),
        ("🔐 Permissions", {
            'fields': (
                'is_active',
                'is_staff',
                'is_superuser',
                'groups',
                'user_permissions',
            ),
        }),
        ("📅 Important Dates", {
            'fields': ('last_login', 'date_joined'),
        }),
    )

    add_fieldsets = (
        ("Create New User", {
            'classes': ('wide',),
            'fields': (
                'email',
                'first_name',
                'last_name',
                'password1',
                'password2',
                'user_type',
                'fund_available',
                'pickup_location',
                'site_region',
                'site_location',
                'contact',
                'is_active',
                'is_staff',
                'is_superuser',
            ),
        }),
    )

    readonly_fields = ('date_joined', 'last_login')

    def colored_name(self, obj):
        color = "#28a745" if obj.user_type == 'admin' else "#007bff"
        return format_html(f"<strong style='color:{color}'>{obj.get_full_name() or obj.email}</strong>")
    colored_name.short_description = "Name"

    def fund_badge(self, obj):
        value = str(obj.fund_available).strip().lower()
        if value == 'yes':
            return format_html('<span style="background-color:#28a745;color:white;padding:4px 8px;border-radius:12px;">Yes</span>')
        else:
            return format_html('<span style="background-color:#dc3545;color:white;padding:4px 8px;border-radius:12px;">No</span>')
    fund_badge.short_description = "Fund Available"

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)
