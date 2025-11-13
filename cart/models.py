from django.db import models
from account.models import User
from products.models import Product  # remove the extra space after 'products'

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_cost(self):
        return self.quantity * self.product.selling_price

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}  - {self.product.name} ({self.quantity})"
