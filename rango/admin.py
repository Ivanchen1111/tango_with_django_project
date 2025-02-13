from django.contrib import admin
from rango.models import Category, Page


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)  # 让 Admin 里显示 `Category` 名称

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url')  # 让 Admin 页面显示这些字段


admin.site.register(Category)
admin.site.register(Page, PageAdmin)

