import uuid
from django.db import models
from datetime import datetime
from account.models import Account


class Item(models.Model):
    class Meta:
        db_table = 'item'
        ordering = ['-updated_date']

    id = models.UUIDField(primary_key=True, db_index=True, unique=True,
                          default=uuid.uuid4)
    name = models.CharField(max_length=100)
    price = models.CharField(max_length=100)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=datetime.now)
    updated_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return self.name

    @classmethod
    def get_items_by_id(cls, item_id) -> 'Item' or None:
        return cls.objects.filter(id=item_id).select_related()

    @classmethod
    def get_items_by_account(cls, account_id) -> 'Item' or None:
        return cls.objects.filter(account=account_id).select_related()

    @classmethod
    def get_items(cls, data: dict) -> 'Item' or None:
        return cls.objects.filter(**data).select_related()
