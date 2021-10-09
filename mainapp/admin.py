from django.contrib import admin
from .models import ProductsCategory, Products
# Register your models here.

admin.site.register(ProductsCategory)


@admin.register(Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'quantity', 'category')
    fields = ('name', 'image', 'description', 'price', 'quantity', 'category')
    readonly_fields = ('description',)
    ordering = ('name', 'price')
    search_fields = ('name',)
