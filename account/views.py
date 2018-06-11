from django.views import View
from django.http import JsonResponse
from account.models import Account


class Token(View):
    @staticmethod
    def get(_, token):
        try:
            status, reason = Account.is_certification(token)
            if status is False:
                raise Exception(reason)

            return JsonResponse({
                'success': status,
            })

        except Exception as e:
            return JsonResponse({
                'success': False,
                'errors': {
                    'field': 'certification',
                    'message': str(e),
                }
            })
