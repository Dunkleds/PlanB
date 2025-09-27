from django.db import models

class Product(models.Model):
    # La columna id_producto es la llave primaria (PK),
    # Django la crea automáticamente como 'id', pero si quieres
    # que coincida con tu base anterior, puedes definirla así:
    # id_producto = models.AutoField(primary_key=True) 
    # Sin embargo, generalmente se recomienda usar el 'id' automático de Django.
    # Usaremos el id automático de Django.

    nombre_producto = models.CharField(max_length=100)
    cantidad = models.IntegerField(default=0)
    
    # numeric(10, 2) se traduce a DecimalField en Django
    precio = models.DecimalField(max_digits=10, decimal_places=2) 
    
    marca = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=500)
    
    # Campo de imagen (URL) que falta en tu tabla original.
    imagen_url = models.URLField(max_length=200, blank=True, null=True)

    class Meta:
        # Esto te permite usar 'Product' en lugar de 'product_product' en consultas
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.nombre_producto