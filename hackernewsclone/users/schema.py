from django.contrib.auth import get_user_model

import graphene
from graphene_django import DjangoObjectType

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model() #no model file needed, Django library has a user model


#Query
class Query(graphene.ObjectType):
    users = graphene.List(UserType)

    def resolve_users(self,info):
        return get_user_model().objects.all()


#CreateUser Mutation
class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True) #Required means they cannot be null values, all values are required.
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
