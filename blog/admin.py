from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Blog, Comment

# =========================
# Blog Admin
# =========================
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author_full_name', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}  # auto-generate slug from title
    search_fields = ('title', 'author__first_name', 'author__last_name', 'content')
    list_filter = ('created_at', 'author')
    ordering = ('-created_at',)

    # Display full name instead of user object
    def author_full_name(self, obj):
        return f"{obj.author.first_name} {obj.author.last_name}"
    author_full_name.short_description = 'Author'

# =========================
# Comment Admin
# =========================
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('blog_title', 'commenter_full_name', 'created_at')
    search_fields = ('content', 'user__first_name', 'user__last_name', 'blog__title')
    list_filter = ('created_at', 'blog')

    # Display blog title
    def blog_title(self, obj):
        return obj.blog.title
    blog_title.short_description = 'Blog'

    # Display full name of commenter
    def commenter_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}"
    commenter_full_name.short_description = 'Commenter'



from django.contrib import admin
from .models import Inquiry

@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at', 'updated_at')
    search_fields = ('name', 'email', 'phone', 'message')
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

