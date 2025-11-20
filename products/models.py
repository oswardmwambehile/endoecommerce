from django.db import models


CATEGORY_CHOICES = [
    ('roofing_sheet', 'Roofing Sheet'),
    ('tiles', 'Tiles'),
]


ROOFING_COLOR_CHOICES = [
    ('red', 'Red'),
    ('blue', 'Blue'),
    ('green', 'Green'),
]

ROOFING_GAUGE_CHOICES = [ 
    ('26', '26'),
    ('28', '28'),
    ('30', '30'),
]

ROOFING_PROFILE_CHOICES = [
    ('corrugated', 'Corrugated'),
    ('ribbed', 'Ribbed'),
]



TILE_COLOR_CHOICES = [
    ('red', 'Red'),
    ('brown', 'Brown'),
    ('gray', 'Gray'),
]
TILE_GAUGE_CHOICES = [ 
    
    ('26', '26'),
   
]

TILE_PROFILE_CHOICES = [
    ('classic', 'Classic'),
    ('Shingle', 'Shingle'),
    ('shake', 'Shake'),
    ('milano', 'Milano'),
]


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # e.g., "Roofing Sheet", "Tiles"

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=200)
    selling_price = models.FloatField()
    discount_price = models.FloatField()
    description = models.TextField()
    product_image = models.ImageField(upload_to='products/')

    def __str__(self):
        return self.name
    

class ProductGauge(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="gauges")
    gauge = models.CharField(max_length=2)  # e.g., '26', '28', '30'
    price_per_meter = models.FloatField()   # price for this gauge

    def __str__(self):
        return f"{self.product.name} - Gauge {self.gauge}"



class RoofingSheetAttribute(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='roofing_attributes')
    color = models.CharField(max_length=50, choices=ROOFING_COLOR_CHOICES)
    profile = models.CharField(max_length=50, choices=ROOFING_PROFILE_CHOICES)

    def __str__(self):
        return f"{self.product.name} - Roofing Attributes"

    def color_choices(self):
        return ROOFING_COLOR_CHOICES

    def profile_choices(self):
        return ROOFING_PROFILE_CHOICES


class TileAttribute(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='tile_attributes')
    color = models.CharField(max_length=50, choices=TILE_COLOR_CHOICES)
    profile = models.CharField(max_length=50, choices=TILE_PROFILE_CHOICES)

    def __str__(self):
        return f"{self.product.name} - Tile Attributes"

    def color_choices(self):
        return TILE_COLOR_CHOICES

    def profile_choices(self):
        return TILE_PROFILE_CHOICES


class MobileSteelAttribute(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='steel_attributes')
    unit_price = models.FloatField(help_text="Price per cubic meter")  # price per m³

    def __str__(self):
        return f"{self.product.name} - Steel Attributes"
