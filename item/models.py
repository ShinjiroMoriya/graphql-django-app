from django.db import models
from datetime import datetime
from account.models import AccountModel


class ItemModel(models.Model):
    class Meta:
        db_table = 'item'

    name = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    account = models.ForeignKey(AccountModel, on_delete=models.CASCADE)
    last_updated = models.DateTimeField(default=datetime.now)
