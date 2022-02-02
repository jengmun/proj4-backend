import uuid
from django.db import models


class Inventory(models.Model):
    product_id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    name = models.CharField(max_length=150)
    description = models.TextField()
    image = models.TextField()
    price = models.PositiveSmallIntegerField()
    cost = models.PositiveIntegerField()
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.name
