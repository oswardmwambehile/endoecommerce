from django.db import models
from account.models import User
from products.models import Product,ProductGauge

class Order(models.Model):
    ORDER_STATUS_CHOICE = (
        ('accepted', 'Accepted'),
        ('packed', 'Packed'),
        ('on_the_way', 'On the way'),
        ('delivered', 'Delivered'),
        ('cancel', 'Cancel'),
        ('pending', 'Pending'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(default=1)
    order_date = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=100, choices=ORDER_STATUS_CHOICE, default='pending')
    price_at_addition = models.FloatField(null=True, blank=True)

    # Optional product attributes
    color = models.CharField(max_length=50, null=True, blank=True)
    profile = models.CharField(max_length=50, null=True, blank=True)
    gauge = models.ForeignKey(ProductGauge, on_delete=models.SET_NULL, null=True, blank=True)
    length = models.FloatField(null=True, blank=True)
    width = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)

    @property
    def total_cost(self):
        # Example: include gauge and steel calculation
        if self.gauge and self.length:
            return self.quantity * self.gauge.price_per_meter * self.length
        steel_attr = getattr(self.product, 'steel_attributes', None)
        if steel_attr and self.length and self.width and self.height:
            volume = self.length * self.width * self.height
            return self.quantity * steel_attr.unit_price * volume
        return self.quantity * self.product.selling_price

    def __str__(self):
        return f"Order #{self.id} - {self.product.name} ({self.quantity}) for {self.user.email}"