import uuid
from django.db import models
from datetime import datetime
from django.contrib.auth.hashers import check_password
from graphqlapp.serializer import serializer_time_loads


class AccountModel(models.Model):

    class Meta:
        db_table = 'account'
        ordering = ['-updated_date']

    id = models.UUIDField(primary_key=True, db_index=True, unique=True,
                          default=uuid.uuid4)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=100, blank=True)
    token = models.UUIDField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    @classmethod
    def get_account(cls, data: dict) -> 'AccountModel' or None:
        return cls.objects.filter(**data).first()

    @classmethod
    def get_accounts(cls, data: dict) -> 'AccountModel' or None:
        return cls.objects.filter(**data)

    @classmethod
    def is_certification(cls, token: str) -> [bool, str]:
        try:
            load_token = serializer_time_loads(token)
            if load_token is None:
                return False, 'Token Invalid'

            account = cls.get_account({'token': load_token})

            if account is None:
                return False, 'Token Invalid'

            if account.is_active is True:
                return False, 'Already Certificated'

            account.is_active = True
            account.save()

            AccountModel.objects.filter(
                email=account.email,
                is_active=False
            ).delete()

            return True, 'success'

        except Exception as e:
            return False, str(e)

    @classmethod
    def is_authenticate(cls, data: dict) -> [bool, 'AccountModel' or None]:
        account = cls.get_account({
            'email': data.get('email'),
            'is_active': True,
        })
        if account is None:
            return False, None

        status = check_password(data.get('password'), account.password)

        return status, account


class AccountTokenModel(models.Model):
    class Meta:
        db_table = 'account_token'
        ordering = ['-created_date']

    id = models.UUIDField(primary_key=True, db_index=True, unique=True,
                          default=uuid.uuid4)
    token = models.CharField(max_length=255)
    account = models.ForeignKey(AccountModel, on_delete=models.CASCADE)
    expire = models.DateTimeField(default=datetime.now)
    created_date = models.DateTimeField(auto_now_add=True)

    @classmethod
    def get_token(cls, data: dict) -> 'AccountTokenModel' or None:
        return cls.objects.filter(**data).first()

    @classmethod
    def get_account(cls, data: dict) -> 'AccountTokenModel' or None:
        data.update({
            'account__is_active': True
        })
        return cls.objects.filter(**data).select_related().first()

    @classmethod
    def get_accounts(cls, data: dict) -> 'AccountTokenModel' or None:
        data.update({
            'account__is_active': True
        })
        return cls.objects.filter(**data).select_related()
