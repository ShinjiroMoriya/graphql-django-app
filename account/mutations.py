import uuid
import graphene
from django.db import transaction
from datetime import datetime, timedelta
from django.core.mail import EmailMessage
from django.contrib.auth.hashers import make_password
from account.models import Account, AccountToken
from account.types import AccountType
from graphqlapp.types import ErrorsType
from graphqlapp.fernet_cipher import fernet
from graphqlapp.serializer import serializer_time_dumps, time_seconds


class Register(graphene.Mutation):
    """
    Mutation to register a account
    """
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        password_confirm = graphene.String(required=True)

    success = graphene.Boolean()
    send_token = graphene.String()
    errors = graphene.List(ErrorsType)
    account = graphene.Field(AccountType)

    @staticmethod
    @transaction.atomic
    def mutate(_, __, **kwargs):
        name = kwargs.get('name')
        email = kwargs.get('email')
        password = kwargs.get('password')
        password_confirm = kwargs.get('password_confirm')

        send_count = Account.objects.filter(
            email=email, is_active=False,
        ).count()

        if send_count >= 3:
            return Register(
                success=False,
                errors=[
                    ErrorsType(
                        field='send email',
                        message='Already sent.'
                    )
                ]
            )

        if password != password_confirm:
            return Register(
                success=False,
                errors=[
                    ErrorsType(
                        field='password',
                        message='Passwords miss match.'
                    )
                ]
            )

        sid = transaction.savepoint()

        try:
            already_account = Account.get_account({
                'email': email, 'is_active': True
            })
            if already_account is not None:
                return Register(
                    success=False,
                    errors=[
                        ErrorsType(
                            field='email',
                            message='Email already registered.'
                        )
                    ]
                )

            active_token = uuid.uuid4()

            account = Account.objects.create(
                name=name,
                email=email,
                password=make_password(password),
                active_token=active_token,
            )
            account.save()

            serialized_token = serializer_time_dumps(
                str(active_token),
                expires=time_seconds(days=1)
            )

            email_message = EmailMessage(
                subject='Register Account',
                from_email='<app@tam-bourine.co.jp>',
                to=[email],
                body="""
                <h3>登録しました。</h3>
                <p><a href="/token/{token}">
                認証してください。(/token/{token})</a></p>
                <p>htmlメール</p>
                """.format(token=str(serialized_token))
            )
            email_message.content_subtype = 'html'
            email_result = email_message.send()
            if email_result != 0:
                return Register(
                    success=True,
                    account=account,
                    send_token=serialized_token,
                )
            else:
                transaction.savepoint_rollback(sid)
                return Register(
                    success=False,
                    errors=[
                        ErrorsType(
                            field='send email',
                            message='Email could not sent'
                        )
                    ]
                )

        except Exception as e:

            transaction.savepoint_rollback(sid)

            return Register(
                success=False,
                errors=[
                    ErrorsType(
                        field='exception',
                        message=str(e)
                    )
                ]
            )


class AccountUpdate(graphene.Mutation):
    """
    Mutation to update a account
    """
    class Arguments:
        token = graphene.String(required=True)
        name = graphene.String()
        email = graphene.String()

    success = graphene.Boolean()
    errors = graphene.List(ErrorsType)
    account = graphene.Field(AccountType)

    @staticmethod
    def mutate(_, __, **kwargs):
        try:
            token = kwargs.get('token')
            account_token = AccountToken.get_account({'token': token})

            account = Account.objects.get(
                id=account_token.account.id,
            )
            name = kwargs.get('name', account.name)
            email = kwargs.get('email', account.email)

            account.name = name
            account.email = email

            account.save()

            return AccountUpdate(
                success=True,
                account=account
            )

        except Exception as e:
            return AccountUpdate(
                success=False,
                errors=[
                    ErrorsType(
                        message=str(e)
                    )
                ]
            )


class Login(graphene.Mutation):
    """
    Mutation to login a account
    """
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    success = graphene.Boolean()
    errors = graphene.List(ErrorsType)
    token = graphene.String()
    expire = graphene.DateTime()

    @staticmethod
    def mutate(_, __, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')

        try:
            status, account = Account.is_authenticate({
                'email': email,
                'password': password,
            })
            if account is None:
                return Login(
                    success=status,
                    errors=[
                        ErrorsType(
                            field='account',
                            message='Account Does not exist'
                        )
                    ]
                )
            if status is True:
                account_token = AccountToken.objects.create(
                    token=fernet.encrypt(str(account.id)),
                    expire=datetime.now() + timedelta(days=1),
                    account=account,
                )
                account_token.save()
                return Login(
                    success=status,
                    token=account_token.token,
                    expire=account_token.expire,
                )
            else:
                return Login(
                    success=status,
                    errors=[
                        ErrorsType(
                            field='password',
                            message='Password Invalid'
                        )
                    ]
                )

        except Exception as e:
            return Login(
                success=False,
                errors=[
                    ErrorsType(
                        field='Exception',
                        message=str(e)
                    )
                ]
            )


class RefreshToken(graphene.Mutation):
    """
    Mutation to re_authenticate a Account
    """
    class Arguments:
        token = graphene.String(required=True)

    success = graphene.Boolean()
    errors = graphene.List(ErrorsType)
    token = graphene.String()
    expire = graphene.DateTime()

    @staticmethod
    def mutate(_, __, token):
        try:
            account_id = fernet.decrypt(token)
            old_account_token = AccountToken.get_accounts(
                {'token': token})
            if len(old_account_token) != 0:
                old_account_token.delete()
            else:
                return RefreshToken(
                    success=False,
                    errors=[
                        ErrorsType(
                            field='token',
                            message='Token does not exist'
                        )
                    ]
                )

            account = Account.get_account({'id': account_id})

            if account is None:
                return RefreshToken(
                    success=False,
                    errors=[
                        ErrorsType(
                            field='account',
                            message='Account does not exist'
                        )
                    ]
                )

            new_token = fernet.encrypt(account.email)
            new_account_token = AccountToken.objects.create(
                token=new_token,
                expire=datetime.now() + timedelta(days=1),
                account=account,
            )
            new_account_token.save()

            return RefreshToken(
                success=True,
                token=new_token,
                expire=new_account_token.expire
            )

        except Exception as e:
            return RefreshToken(
                success=False,
                errors=[
                    ErrorsType(
                        field='exception',
                        message=str(e)
                    )
                ],
            )


class AccountByToken(graphene.Mutation):
    """
    Mutation for Get Account Data
    """
    class Arguments:
        token = graphene.String(required=True)

    success = graphene.Boolean()
    errors = graphene.List(ErrorsType)
    account = graphene.Field(AccountType)

    @staticmethod
    def mutate(_, __, token):
        try:
            account = AccountToken.get_account({'token': token})
            if account is None:
                return AccountByToken(
                    success=False,
                    errors=[
                        ErrorsType(
                            field='token',
                            message='Token Does not exist'
                        )
                    ]
                )

            if account.expire < datetime.now():

                account.delete()

                return AccountByToken(
                    success=False,
                    errors=[
                        ErrorsType(
                            field='expired',
                            message='It has expired'
                        )
                    ]
                )

            return AccountByToken(
                success=True,
                account=account.account
            )

        except Exception as e:
            return AccountByToken(
                success=False,
                errors=[
                    ErrorsType(message=str(e))
                ]
            )


class ResetPassword(graphene.Mutation):
    """
    Mutation for requesting a password reset email
    """
    class Arguments:
        email = graphene.String(required=True)

    success = graphene.Boolean()
    errors = graphene.List(ErrorsType)
    send_token = graphene.String()
    account = graphene.Field(AccountType)

    @staticmethod
    @transaction.atomic
    def mutate(_, __, email):

        sid = transaction.savepoint()

        try:
            account = Account.get_account({'email': email})
            if account is None:
                return ResetPassword(
                    success=False,
                    errors=[
                        ErrorsType(
                            field='email',
                            message='Account Does not exist'
                        )
                    ]
                )
            uuid_token = uuid.uuid4()
            account.password_token = uuid_token
            account.save()

            serialized_token = serializer_time_dumps(
                str(uuid_token),
                expires=time_seconds(days=1)
            )

            email_message = EmailMessage(
                subject='Register Account',
                from_email='<app@tam-bourine.co.jp>',
                to=[email],
                body="""
                <h3>変更手続きをしてください。</h3>
                <p><a href="/password/{token}">
                認証してください。(/password/{token})</a></p>
                <p>htmlメール</p>
                """.format(token=str(serialized_token))
            )
            email_message.content_subtype = 'html'
            email_result = email_message.send()
            if email_result != 0:
                return ResetPassword(
                    success=True,
                    account=account,
                    send_token=serialized_token
                )
            else:
                transaction.savepoint_rollback(sid)
                return ResetPassword(
                    success=False,
                    errors=[
                        ErrorsType(
                            field='send email',
                            message='Email could not sent'
                        )
                    ]
                )

        except Exception as e:
            transaction.savepoint_rollback(sid)
            return ResetPassword(
                success=False,
                errors=['email', str(e)]
            )


class ResetPasswordConfirm(graphene.Mutation):
    """
    Mutation for requesting a password reset email
    """

    class Arguments:
        uid = graphene.String(required=True)
        token = graphene.String(required=True)
        email = graphene.String(required=True)
        new_password = graphene.String(required=True)
        re_new_password = graphene.String(required=True)

    success = graphene.Boolean()
    errors = graphene.List(ErrorsType)

    @staticmethod
    def mutate(_, __, **kwargs):
        return ResetPasswordConfirm(success=True, errors=None)


class DeleteAccount(graphene.Mutation):
    """
    Mutation to delete an account
    """
    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    success = graphene.Boolean()
    errors = graphene.List(graphene.String)

    @staticmethod
    def mutate(_, info, email, password):
        is_authenticated = info.context.user.is_authenticated
        if not is_authenticated:
            errors = ['unauthenticated']
        elif is_authenticated and not email == info.context.user.email:
            errors = ['forbidden']
        elif not info.context.user.check_password(password):
            errors = ['wrong password']
        else:
            info.context.user.delete()
            return DeleteAccount(success=True)
        return DeleteAccount(success=False, errors=errors)
