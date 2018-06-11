import graphene
from graphene_django.debug import DjangoDebug
from item.query import ItemQuery
from account.mutations import (
    Register, Login, Logout,RefreshToken, AccountByToken, ActivateAccount,
    AccountUpdate, ResetPassword, ResetPasswordConfirm, DeleteAccount
)


class Query(ItemQuery, graphene.ObjectType):
    pass


class Mutations(graphene.ObjectType):
    register = Register.Field(
        description='新規登録'
    )
    activate_account = ActivateAccount.Field(
        description='アカウント認証'
    )
    login = Login.Field(
        description='ログイン'
    )
    logout = Logout.Field(
        description='ログアウト'
    )
    refresh_token = RefreshToken.Field(
        description='リフレッシュトークン'
    )
    account_by_token = AccountByToken.Field(
        description='アカウントデータ取得'
    )
    account_update = AccountUpdate.Field(
        description='アカウントデータ更新'
    )
    reset_password = ResetPassword.Field(
        description='パスワードの変更'
    )
    reset_password_confirm = ResetPasswordConfirm.Field(
        description='パスワードの変更確認'
    )
    delete_account = DeleteAccount.Field(
        description='アカウント削除'
    )
    debug = graphene.Field(DjangoDebug)


schema = graphene.Schema(query=Query, mutation=Mutations)
