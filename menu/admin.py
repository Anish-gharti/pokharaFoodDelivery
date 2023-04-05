from django.contrib import admin
from .models import Category, FoodItem
# Register your models here.

class Categoryadmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'vendor', 'updated_at')
    search_fields = ('category_name', 'vendor__vendor_name__exact')

class FoodItemAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('food_item',)}
    list_display = ('food_item', 'category', 'vendor', 'price', 'is_available', 'updated_at')
    search_fields = ('food_item', 'category__category_name__icontains', 'vendor__vendor_name__exact', 'is_available')


admin.site.register(Category, Categoryadmin)
admin.site.register(FoodItem, FoodItemAdmin)

