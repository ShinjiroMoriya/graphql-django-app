from django.views import View
from django.template.response import TemplateResponse


class Home(View):
    @staticmethod
    def get(request):
        return TemplateResponse(request, 'index.html')
