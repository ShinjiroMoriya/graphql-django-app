import graphene


class ErrorsType(graphene.ObjectType):
    field = graphene.String()
    message = graphene.String()
