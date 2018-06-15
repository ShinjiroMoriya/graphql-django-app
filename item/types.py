from graphene_django import DjangoObjectType
from item.models import Item
from graphene import Node


class ItemType(DjangoObjectType):
    class Meta:
        model = Item
        description = " Type definition for a single Item "
        filter_fields = {
            'id': ['exact'],
            'name': ['exact', 'icontains', 'iexact'],
            'price': ['exact', 'icontains', 'iexact'],
            'image': ['exact'],
            'account': ['exact'],
            'recommended': ['exact'],
            'updated_date': ['exact', 'icontains', 'iexact'],
            'created_date': ['exact', 'icontains', 'iexact'],
        }
        interfaces = (Node,)
