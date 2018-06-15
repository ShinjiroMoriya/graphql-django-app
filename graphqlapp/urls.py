from django.urls import path
from django.views.generic import TemplateView
from graphene_django.views import GraphQLView
from graphqlapp.schema import schema


urlpatterns = [
    path('graphql', GraphQLView.as_view(graphiql=True, schema=schema)),
    path('favicon.ico', TemplateView.as_view(template_name='favicon.ico')),
]
