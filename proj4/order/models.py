import uuid
from django.contrib.postgres.fields import ArrayField
from django.db import models


# class Order(models.Model):
#     order_no = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
#     date = models.DateTimeField(auto_now_add=True)
#     customer = models.ForeignKey('account.Account', on_delete=models.DO_NOTHING())
#     order_details = ArrayField(models.JSONField())
#
#     def __str__(self):
#         return self.order_no
