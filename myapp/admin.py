from django.contrib import admin
from .models import Product, Movement

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'product_code', 'quantity', 'unit', 'min_stock')
    search_fields = ('product_name', 'product_code')

@admin.register(Movement)
class MovementAdmin(admin.ModelAdmin):
    list_display = ('product', 'movement_type', 'quantity', 'date')  # تم التعديل هنا
