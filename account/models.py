from django.db import models
from datetime import datetime


class AccountModel(models.Model):
    class Meta:
        db_table = 'account'

    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    last_updated = models.DateTimeField(default=datetime.now)
