from django.contrib import admin
from .models import CartItem, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("nombre_producto", "marca", "precio", "cantidad")
    search_fields = ("nombre_producto", "marca")


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "quantity", "added_at")
    search_fields = ("user__username", "product__nombre_producto")
    list_filter = ("added_at",)
