from decimal import Decimal

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CartItem, Product
from .serializers import (
    CartItemAddSerializer,
    CartItemSerializer,
    CartItemSetSerializer,
    ProductSerializer,
)


def _cart_payload_for(user):
    items = list(
        CartItem.objects.filter(user=user)
        .select_related("product")
        .order_by("-added_at")
    )
    serializer = CartItemSerializer(items, many=True)
    total_quantity = sum(item.quantity for item in items)
    total_amount = sum((Decimal(item.quantity) * item.product.precio for item in items), Decimal("0"))

    return {
        "items": serializer.data,
        "summary": {
            "total_quantity": total_quantity,
            "total_amount": str(total_amount),
        },
    }


class ProductListView(APIView):
    permission_classes = [AllowAny]

    def get(self, _request):
        products = Product.objects.all().order_by("nombre_producto")
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class CartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(_cart_payload_for(request.user))

    def post(self, request):
        serializer = CartItemAddSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = serializer.validated_data["product"]
        quantity = serializer.validated_data["quantity"]

        item, created = CartItem.objects.get_or_create(
            user=request.user,
            product=product,
            defaults={"quantity": quantity},
        )
        if not created:
            item.quantity += quantity
            item.save(update_fields=["quantity"])

        return Response(_cart_payload_for(request.user), status=status.HTTP_200_OK)


class CartItemDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, product_id: int):
        serializer = CartItemSetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quantity = serializer.validated_data["quantity"]

        try:
            item = CartItem.objects.get(user=request.user, product_id=product_id)
        except CartItem.DoesNotExist:
            return Response({"detail": "Producto no encontrado en tu carrito."}, status=status.HTTP_404_NOT_FOUND)

        if quantity == 0:
            item.delete()
        else:
            item.quantity = quantity
            item.save(update_fields=["quantity"])

        return Response(_cart_payload_for(request.user))

    def delete(self, request, product_id: int):
        deleted, _ = CartItem.objects.filter(user=request.user, product_id=product_id).delete()
        status_code = status.HTTP_200_OK if deleted else status.HTTP_404_NOT_FOUND
        payload = _cart_payload_for(request.user)
        return Response(payload, status=status_code)
