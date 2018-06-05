from django.http import HttpResponse
from django.views import View


class Home(View):
    @staticmethod
    def get(_):
        response = HttpResponse('Graphql Django App')
        return response
