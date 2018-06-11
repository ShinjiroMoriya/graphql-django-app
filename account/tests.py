from django.test import TestCase
from django.test.client import Client
from graphqlapp.schema import schema
from account.models import Account
from django.contrib.auth.hashers import make_password


class AccountTests(TestCase):

    login_query = """
    mutation(
        $email: String!,
        $password: String!
    ) {
        login (
            email: $email,
            password: $password
        ) {
            expire
            token
            success
            errors {
                field
                message
            }
        }
    }
    """

    activate_query = """
    mutation(
        $token: String!,
    ) {
        activateAccount (
            token: $token
        ) {
            success
            errors {
                field
                message
            }
        }
    }
    """

    logout_query = """
    mutation(
        $token: String!,
    ) {
        logout (
            token: $token
        ) {
            success
            errors {
                field
                message
            }
        }
    }
    """

    register_query = """
    mutation(
        $name: String!,
        $email: String!,
        $password: String!,
        $passwordConfirm: String!
    ) {
        register (
            name: $name,
            email: $email,
            password: $password,
            passwordConfirm: $passwordConfirm
        ) {
            account {
                name
            }
            sendToken
            success
            errors {
                field
                message
            }
        }
    }
    """

    update_query = """
    mutation(
        $token: String!,
        $name: String!
    ) {
        accountUpdate (
            token: $token
            name: $name
        ) {
            account {
                id
                name
                email
            }
            success
            errors {
                field
                message
            }
        }
    }
    """

    account_by_token_query = """
    mutation(
        $token: String!
    ) {
        accountByToken(
            token: $token
        ) {
            account {
                name
                email
                isActive
                createdDate
                updatedDate
            }
            success
            errors {
                message
            }
        }
    }
    """

    reset_password_query = """
    mutation(
        $email: String!
    ) {
        resetPassword(
            email: $email
        ) {
            success
            sendToken
            errors {
                field
                message
            }
            account {
                passwordToken
            }
        }
    }
    """

    reset_password_confirm_query = """
    mutation(
        $token: String!,
        $password: String!,
        $passwordConfirm: String!
    ) {
        resetPasswordConfirm(
            token: $token,
            password: $password,
            passwordConfirm: $passwordConfirm
        ) {
            success
            errors {
                field
                message
            }
        }
    }
    """

    delete_query = """
    mutation(
        $email: String!,
        $password: String!
    ) {
        deleteAccount(
            email: $email,
            password: $password        
        ) {
            success
            errors {
                field
                message
            }
        }
    }
    """

    @classmethod
    def setUpTestData(cls):
        account = Account.objects.create(
            name='test_taro',
            email='moriya+test@tam-bourine.co.jp',
            password=make_password('02080208'),
            is_active=True,
        )
        account.save()

        account = Account.objects.create(
            name='test_jiro',
            email='moriya+dev@tam-bourine.co.jp',
            password=make_password('02080208'),
            is_active=True,
        )
        account.save()

    def setUp(self):
        self.client = Client()

    def test_login_mutation_success(self):
        result = schema.execute(
            self.login_query,
            variable_values={
                'email': 'moriya+test@tam-bourine.co.jp',
                'password': '02080208',
            }
        )
        """
        result
        {
            'login': {
                'expire: '2018-06-09T15:39:08.998708',
                'token: 'gAAAAABbGiSMy39SNz_oXZsgryR...',
                'success': True,
                'errors': None
            }
        }
        """
        assert result.data['login']['errors'] is None
        assert result.data['login']['token'] is not None
        assert result.data['login']['success'] is True

    def test_logout_mutation_success(self):
        login_result = schema.execute(
            self.login_query,
            variable_values={
                'email': 'moriya+test@tam-bourine.co.jp',
                'password': '02080208',
            }
        )
        token = login_result.data['login']['token']
        result = schema.execute(
            self.logout_query,
            variable_values={
                'token': token,
            }
        )
        assert result.data['logout']['errors'] is None
        assert result.data['logout']['success'] is True

    def test_register_mutation_success(self):
        result = schema.execute(
            self.register_query,
            variable_values={
                'name': 'sample',
                'email': 'moriya+12345@tam-bourine.co.jp',
                'password': '02080208',
                'passwordConfirm': '02080208',
            }
        )
        """
        result
        {
            'register': {
                'account': {
                    'token': 'fd9ae8ee-9284-4e15-8490-2f9734da3315',
                }
                'sendToken': 'eyJhbGciOiJIUzI1NiIsImlhdCI6MTUyODQ0...',
                'success': True,
                'errors': None
            }
        }
        """
        assert result.data['register']['errors'] is None
        assert result.data['register']['sendToken'] is not None
        assert result.data['register']['success'] is True

    def test_activate_account_success(self):
        register_result = schema.execute(
            self.register_query,
            variable_values={
                'name': 'sample',
                'email': 'moriya+12345@tam-bourine.co.jp',
                'password': '02080208',
                'passwordConfirm': '02080208',
            }
        )

        token = register_result.data['register']['sendToken']

        result = schema.execute(
            self.activate_query,
            variable_values={
                'token': token,
            }
        )

        assert result.data['activateAccount']['errors'] is None
        assert result.data['activateAccount']['success'] is True

    def test_account_update_mutation_success(self):
        before_data = Account.get_account(
            {'email': 'moriya+test@tam-bourine.co.jp'}
        )

        before_name = before_data.name

        login_result = schema.execute(
            self.login_query,
            variable_values={
                'email': 'moriya+test@tam-bourine.co.jp',
                'password': '02080208',
            }
        )
        token = login_result.data['login']['token']

        result = schema.execute(
            self.update_query,
            variable_values={
                'token': token,
                'name': 'test_sample',
            }
        )
        """
        result
        {
            'accountUpdate': {
                'account': {
                    'id': '108c4f0a-c3cb-4c8e-b3c5-1c6f9f20edce',
                    'name': 'test_sample',
                    'email': 'moriya+test@tam-bourine.co.jp'
                },
                'success': True,
                'errors': None
            }
        }
        """
        assert result.data['accountUpdate']['account']['name'] != before_name

    def test_get_account_by_token_mutation_success(self):
        login_result = schema.execute(
            self.login_query,
            variable_values={
                'email': 'moriya+test@tam-bourine.co.jp',
                'password': '02080208',
            }
        )

        token = login_result.data['login']['token']

        result = schema.execute(
            self.account_by_token_query,
            variable_values={
                'token': token,
            }
        )
        """
        result
        {
            'accountByToken': {
                'account': {
                    'name': 'test_taro',
                    'email': 'moriya+test@tam-bourine.co.jp',
                    'isActive': True,
                    'createdDate': '2018-06-08T16:23:51.179307',
                    'updatedDate', '2018-06-08T16:23:51.179585',
                }
                'success: True,
                'errors': None
            }
        }
        """
        assert result.data['accountByToken']['errors'] is None
        assert result.data['accountByToken']['account'] is not None
        assert result.data['accountByToken']['success'] is True

    def test_reset_password_mutation_success(self):
        result = schema.execute(
            self.reset_password_query,
            variable_values={
                'email': 'moriya+test@tam-bourine.co.jp',
            }
        )
        """
        result
        {
            'resetPassword': {
                'account': {
                    'passwordToken': 'ca395f4e-c603-4221-8fe2-c7135b7c5293',
                }
                'sendToken': 'eyJhbGciOiJIUzI1NiIsImlhdCI6MTUyODY5N...',
                'success: True,
                'errors': None
            }
        }
        """
        assert result.data['resetPassword']['errors'] is None
        assert result.data['resetPassword']['sendToken'] is not None
        assert result.data['resetPassword']['success'] is True

    def test_reset_password_confirm_mutation_success(self):
        send_result = schema.execute(
            self.reset_password_query,
            variable_values={
                'email': 'moriya+test@tam-bourine.co.jp',
            }
        )
        token = send_result.data['resetPassword']['sendToken']
        password_result = schema.execute(
            self.reset_password_confirm_query,
            variable_values={
                'token': token,
                'password': "qwerty1234",
                'passwordConfirm': "qwerty1234"
            }
        )
        assert password_result.data['resetPasswordConfirm']['errors'] is None
        assert password_result.data['resetPasswordConfirm']['success'] is True

        login_result = schema.execute(
            self.login_query,
            variable_values={
                'email': 'moriya+test@tam-bourine.co.jp',
                'password': 'qwerty1234',
            }
        )

        assert login_result.data['login']['errors'] is None
        assert login_result.data['login']['success'] is True

    def test_delete_mutation_success(self):
        result = schema.execute(
            self.delete_query,
            variable_values={
                'email': 'moriya+dev@tam-bourine.co.jp',
                'password': '02080208',
            }
        )
        assert result.data['deleteAccount']['errors'] is None
        assert result.data['deleteAccount']['success'] is True
