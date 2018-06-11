import graphene
from graphene_django.debug import DjangoDebug
from item.query import ItemQuery
from account.mutations import (
    Register, Login, RefreshToken,
    AccountByToken, AccountUpdate, ResetPassword
)


class Query(ItemQuery, graphene.ObjectType):
    pass


class Mutations(graphene.ObjectType):
    register = Register.Field(description='新規登録')
    login = Login.Field(description='ログイン')
    refresh_token = RefreshToken.Field(description='リフレッシュトークン')
    account_by_token = AccountByToken.Field(description='アカウントデータ取得')
    account_update = AccountUpdate.Field(description='アカウントデータ更新')
    reset_password = ResetPassword.Field(description='パスワードの変更')
    debug = graphene.Field(DjangoDebug)


schema = graphene.Schema(query=Query, mutation=Mutations)
