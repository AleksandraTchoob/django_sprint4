from django.contrib import admin
from .models import Category, Location, Post


# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'created_at')
    list_filter = ('is_published',)
    search_fields = ('title',)
    list_editable = ('is_published',)


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_published', 'created_at')
    list_filter = ('is_published',)
    search_fields = ('name',)
    list_editable = ('is_published',)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'pub_date', 'author',
                    'category', 'location', 'is_published')
    list_filter = ('category', 'is_published', 'pub_date')
    search_fields = ('title', 'text')
    list_editable = ('is_published', 'category', 'location')
    date_hierarchy = 'pub_date'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
