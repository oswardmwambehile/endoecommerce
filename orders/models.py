from django.db import models
from account.models import User
from products.models import Product

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
    updated_at = models.DateTimeField(auto_now=True)  # <-- Track last update
    status = models.CharField(max_length=100, choices=ORDER_STATUS_CHOICE, default='pending')

    @property
    def total_cost(self):
        return self.quantity * self.product.selling_price

    def __str__(self):
        return f"Order #{self.id} - {self.product.name} ({self.quantity}) for {self.user.email}"
