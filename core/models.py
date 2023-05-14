from uuid import uuid4

from django.db import models


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=1024)
    description = models.TextField()


class Offer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    items_in_stock = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="offers")
