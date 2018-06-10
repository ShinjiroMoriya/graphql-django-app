from account.models import AccountModel
from graphene_django import DjangoObjectType


class AccountType(DjangoObjectType):
    class Meta:
        model = AccountModel
        description = " Type definition for a single Account "
        filter_fields = {
            'id': ['exact'],
            'name': ['exact', 'icontains', 'iexact'],
            'email': ['exact', 'icontains', 'iexact'],
            'password': ['exact', 'icontains', 'iexact'],
            'is_active': ['exact', 'icontains', 'iexact'],
            'token': ['exact', 'icontains', 'iexact'],
            'updated_date': ['exact', 'icontains', 'iexact'],
            'created_date': ['exact', 'icontains', 'iexact'],
        }
        exclude_fields = ('password',)
