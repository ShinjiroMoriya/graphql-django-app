from django.urls import path
from django.views.generic import TemplateView
from graphene_django.views import GraphQLView
from graphqlapp.schema import schema
from item.views import Home
from account.views import Token


urlpatterns = [
    path('', Home.as_view()),
    path('graphql', GraphQLView.as_view(graphiql=True, schema=schema)),
    path('token/<token>', Token.as_view()),
    path('favicon.ico', TemplateView.as_view(template_name='favicon.ico')),
]
