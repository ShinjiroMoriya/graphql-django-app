from django.urls import path
from graphene_django_extras.views import ExtraGraphQLView
from graphqlapp.schema import schema
from item.views import Home
urlpatterns = [
    path('', Home.as_view()),
    path('graphql', ExtraGraphQLView.as_view(graphiql=True, schema=schema)),
]
