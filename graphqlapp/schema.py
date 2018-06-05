from item.models import ItemModel
from account.models import AccountModel
import graphene
from graphene_django_extras import (
    DjangoObjectType, DjangoObjectField, DjangoFilterPaginateListField,
    DjangoSerializerMutation,
)
from graphene_django_extras.paginations import LimitOffsetGraphqlPagination

import graphqlapp.serializers as serializers
from graphene_django.debug import DjangoDebug


class AccountType(DjangoObjectType):
    class Meta:
        model = AccountModel
        description = " Type definition for a single Account "
        filter_fields = {
            'id': ['exact', ],
            'name': ['exact', 'icontains', 'iexact'],
            'email': ['exact', 'icontains', 'iexact'],
            'last_updated': ['icontains', 'iexact'],
        }


class ItemType(DjangoObjectType):
    class Meta:
        model = ItemModel
        description = " Type definition for a single Item "
        filter_fields = {
            'id': ['exact', ],
            'name': ['exact', 'icontains', 'iexact'],
            'price': ['exact', 'icontains', 'iexact'],
            'account': ['exact'],
            'last_updated': ['exact', 'icontains', 'iexact'],
        }


class Query(graphene.ObjectType):
    item = DjangoObjectField(ItemType, description='Single Item query')
    items = DjangoFilterPaginateListField(
        ItemType, pagination=LimitOffsetGraphqlPagination(default_limit=25)
    )
    account = DjangoObjectField(AccountType, description='Single Account query')
    accounts = DjangoFilterPaginateListField(
        AccountType, pagination=LimitOffsetGraphqlPagination(default_limit=25)
    )
    debug = graphene.Field(DjangoDebug, name='__debug')


class AccountSerializerMutation(DjangoSerializerMutation):
    class Meta:
        description = "DRF serializer based Mutation for Account "
        serializer_class = serializers.AccountSerializer


class ItemSerializerMutation(DjangoSerializerMutation):
    class Meta:
        description = "DRF serializer based Mutation for Items "
        serializer_class = serializers.ItemSerializer


class Mutations(graphene.ObjectType):
    item_create = ItemSerializerMutation.CreateField()
    item_delete = ItemSerializerMutation.DeleteField()
    item_update = ItemSerializerMutation.UpdateField()

    account_create = AccountSerializerMutation.CreateField()
    account_delete = AccountSerializerMutation.DeleteField()
    account_update = AccountSerializerMutation.UpdateField()

    debug = graphene.Field(DjangoDebug, name='__debug')


schema = graphene.Schema(query=Query, mutation=Mutations)
