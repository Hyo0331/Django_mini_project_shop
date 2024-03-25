from django.contrib import admin
from .models import Yarn, Category, Manufacturer, Tag, Comment
from markdownx.admin import MarkdownxModelAdmin

# Register your models here.

admin.site.register(Yarn, MarkdownxModelAdmin)

class CategoryAdmin(admin.ModelAdmin) :
    prepopulated_fields = {'slug': ('name', )}

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Comment)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Manufacturer)
admin.site.register(Tag, TagAdmin)