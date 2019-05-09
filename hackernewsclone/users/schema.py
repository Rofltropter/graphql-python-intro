from django.contrib.auth import get_user_model

import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q

class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model() #no model file needed, Django library has a user model


#Query
class Query(graphene.ObjectType):
    users = graphene.List(UserType, username_search = graphene.String(), id_search = graphene.Int(), email_search = graphene.String())
    me = graphene.Field(UserType)

    def resolve_users(self, info, username_search = None, id_search = None, email_search = None):
        qs = get_user_model().objects.all()

        if username_search:
            filter = (Q(username__iexact = username_search) | Q(username__icontains = username_search))  #Additional Section added by me. Queries username based on exact match or if search is contained within username
            qs = qs.filter(filter)

        if id_search:
            filter = Q(id__exact = id_search)
            qs = qs.filter(filter)

        if email_search:
            filter = Q(email__icontains = email_search)
            qs = qs.filter(filter)

        return qs

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous: #ie. user is not logged in
            raise Exception('Not logged in!')

        return user

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
