from decimal import Decimal

from rest_framework import serializers

from .models import CartItem, Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "nombre_producto",
            "cantidad",
            "precio",
            "marca",
            "descripcion",
            "imagen_url",
        )


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    line_total = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = (
            "id",
            "product",
            "quantity",
            "line_total",
        )

    def get_line_total(self, obj: CartItem) -> str:
        total = Decimal(obj.quantity) * obj.product.precio
        return str(total)


class CartItemAddSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, default=1)

    def validate(self, attrs):
        product_id = attrs.get("product_id")
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist as exc:  # pragma: no cover - simple validation
            raise serializers.ValidationError({"product_id": "Producto no encontrado."}) from exc

        attrs["product"] = product
        return attrs


class CartItemSetSerializer(serializers.Serializer):
    quantity = serializers.IntegerField(min_value=0)

