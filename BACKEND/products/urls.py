from django.urls import path

from .views import CartItemDetailView, CartView, ProductListView

app_name = "products"

urlpatterns = [
    path("products/", ProductListView.as_view(), name="product_list"),
    path("cart/", CartView.as_view(), name="cart"),
    path("cart/<int:product_id>/", CartItemDetailView.as_view(), name="cart_item"),
]
