import graphene
from datetime import datetime
from graphene_django.debug import DjangoDebug
from item.types import ItemType
from account.models import AccountToken
from graphqlapp.fernet_cipher import fernet
from item.models import Item


class ItemQuery(graphene.ObjectType):

    item = graphene.Field(
        ItemType,
        description='get Item',
        token=graphene.String(default_value=None),
        item_id=graphene.String(default_value=None)
    )

    @staticmethod
    def resolve_item(_, __, **kwargs):
        token = kwargs.get('token')
        if token is None:
            return None

        account_token = AccountToken.get_token({'token': token})

        if account_token.expire < datetime.now():
            return None

        item_id = kwargs.get('item_id')
        if item_id is not None:
            return Item.get_items({'id': item_id}).first()
        return None

    items = graphene.List(
        ItemType,
        limit=graphene.Int(default_value=25),
        offset=graphene.Int(default_value=0),
        token=graphene.String(default_value=None)
    )

    @staticmethod
    def resolve_items(_, __, **kwargs):
        token = kwargs.get('token')
        if token is None:
            return None

        account_token = AccountToken.get_token({'token': token})

        if account_token.expire < datetime.now():
            return None

        account_id = fernet.decrypt(token)

        if account_id is not None:
            return Item.get_items({'account': account_id}).select_related()

        return None

    debug = graphene.Field(DjangoDebug)
