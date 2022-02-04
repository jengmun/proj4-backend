import uuid
from django.db import models


class Order(models.Model):
    order_no = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey('account.Account', on_delete=models.DO_NOTHING)

    def __str__(self):
        return str(self.order_no)


class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    price = models.PositiveSmallIntegerField()
    cost = models.PositiveIntegerField()
    quantity = models.PositiveSmallIntegerField()
    item = models.ForeignKey('inventory.Inventory', on_delete=models.DO_NOTHING)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)
