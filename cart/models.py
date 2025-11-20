from django.db import models
from account.models import User
from products.models import Product, ProductGauge

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    # Roofing / Tiles
    color = models.CharField(max_length=50, null=True, blank=True)
    profile = models.CharField(max_length=50, null=True, blank=True)
    gauge = models.ForeignKey(ProductGauge, on_delete=models.SET_NULL, null=True, blank=True)
    length = models.FloatField(null=True, blank=True)
    
    # Steel
    width = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)

    quantity = models.PositiveIntegerField(default=1)
    price_at_addition = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """
        Ensure all numeric inputs are floats and set price_at_addition correctly.
        """
        # Convert numeric fields to float
        for field in ['length', 'width', 'height', 'quantity']:
            val = getattr(self, field)
            try:
                setattr(self, field, float(val) if val not in [None, ''] else 0)
            except (ValueError, TypeError):
                setattr(self, field, 0)

        # Set price_at_addition
        if self.price_at_addition is None:
            # Roofing / Tiles: use gauge price if available
            if self.gauge and self.gauge.price_per_meter is not None:
                self.price_at_addition = float(self.gauge.price_per_meter)
            # Steel product: use unit price per m³
            elif getattr(self.product, 'steel_attributes', None):
                self.price_at_addition = float(self.product.steel_attributes.unit_price or 0)
            # Other products: fallback to product selling price
            else:
                self.price_at_addition = float(self.product.selling_price or 0)

        super().save(*args, **kwargs)

    @property
    def unit_price(self):
        """Return the price per unit (gauge price or steel unit price)."""
        return float(self.price_at_addition or 0)

    @property
    def total_cost(self):
        """Calculate total cost based on product type and input dimensions."""
        length = float(self.length or 0)
        width = float(self.width or 0)
        height = float(self.height or 0)
        quantity = float(self.quantity or 1)

        # Roofing / Tiles: price per meter × length × quantity
        if self.gauge and length > 0:
            return self.unit_price * length * quantity

        # Steel product: price per m³ × volume × quantity
        steel_attr = getattr(self.product, 'steel_attributes', None)
        if steel_attr and length > 0 and width > 0 and height > 0:
            volume = length * width * height
            return self.unit_price * volume * quantity

        # Other products: simple unit price × quantity
        return self.unit_price * quantity

    def __str__(self):
        desc = f"{self.product.name} (x{int(self.quantity)})"
        if self.color:
            desc += f" - {self.color}"
        if self.profile:
            desc += f" / {self.profile}"
        if self.gauge:
            desc += f" - Gauge {self.gauge.gauge}"
        return desc
