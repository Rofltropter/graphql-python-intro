import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q      #for querying

from users.schema import UserType
from .models import Link, Vote

from graphql import GraphQLError

class LinkType(DjangoObjectType):
    class Meta:
        model = Link

class VoteType(DjangoObjectType):
    class Meta:
        model = Vote

class Query(graphene.ObjectType):
    links = graphene.List(LinkType, search=graphene.String(), first=graphene.Int(), skip=graphene.Int())  # "links" is the query root key. It's also what the query returns, a full Links so the user can ask for the field it wants. "search" is our search parameter
    votes = graphene.List(VoteType)

    def resolve_links(self, info, search = None, first = None, skip = None, **kwargs):     #val set in search parameter will be the args var
        qs = Link.objects.all()

        if search:
            filter = (Q(url__icontains=search) | Q(description__icontains=search))     #filter against url's and descriptions
            qs = qs.filter(filter)         # searches by filter requirements, displays ALL matches, by order of id(ie. order of creation)

        if skip:
            qs = qs[skip::]   #starts at skip slice, skips the first "skip" slices

        if first:
            qs = qs[:first]             #end slice is first, gives the first "first" values available.

        return qs             #order matters, since skip must come before first to ensure proper values are being delivered

    def resolve_votes(self, info, **kwargs):
        return Vote.objects.all()

#In the snipped above, LinkType was created using the DjangoObjectType - a custom type available in Graphene Django
#Also, the special type query was created with a resolver for the field links, which returns all the links. self= context, **kwargs = args provided to the field in the GraphQL query
# See more about the .objects.... in the django QuerySet Documentation: https://docs.djangoproject.com/en/2.1/ref/models/querysets/#all

#1
class CreateLink(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()
    posted_by = graphene.Field(UserType)

    #2   now to define the CreateLink arguments, ie. the data you can send to the server as a client making a create_link mutation request
    class Arguments:
        url = graphene.String()
        description = graphene.String()

    #3
    def mutate(self, info, url, description):
        user = info.context.user or None    #Defines the current user creating the link with info.context.user or server side no user creation
        link = Link(url=url, description=description, posted_by=user)  #creates a new link with the passed url, description, and which user created it
        link.save()  #saves the link

        #available values to return
        return CreateLink(
            id =link.id,
            url=link.url,
            description=link.description,
            posted_by=link.posted_by,
        )

class CreateVote(graphene.Mutation):
    user = graphene.Field(UserType)
    link = graphene.Field(LinkType)

    class Arguments:
        link_id = graphene.Int()

    def mutate(self, info, link_id):
        user = info.context.user
        if user.is_anonymous:
            raise GraphQLError('You must be logged in to vote!')

        link = Link.objects.filter(id=link_id).first()      #filters for Link objects with the link_id id value and selects the first one it finds
        if not link:
            raise GraphQLError('Invalid link!')

        #actually goes and creates the Vote object
        Vote.objects.create(
            user=user,
            link=link,
        )

        return CreateVote(user=user, link=link)



class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()
    create_vote = CreateVote.Field()

#1: Defines a mutation class. Right after, you define the output of the mutation, the data the server can send back to the client.
# The output is defined field by field for learning purposes. In the next mutation you’ll define them as just one.
#2: Defines the data you can send to the server, in this case, the links’ url and description.
#3: The mutation method: it creates a link in the database using the data sent by the user, through the url and description parameters.
# After, the server returns the CreateLink class with the data just created. See how this matches the parameters set on #1.


