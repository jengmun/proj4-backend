from django.db import models


class Cart(models.Model):
    cart_item = models.ForeignKey('inventory.Inventory', on_delete=models.CASCADE)
    cart_owner = models.ForeignKey('account.Account', on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.cart_owner}, {self.cart_item}'
