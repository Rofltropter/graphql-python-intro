import graphene
from graphene_django import DjangoObjectType
from users.schema import UserType

from .models import Link

class LinkType(DjangoObjectType):
    class Meta:
        model = Link

class Query(graphene.ObjectType):
    links = graphene.List(LinkType) # "links" is the query root key. It's also what the query returns, a full Links so the user can ask for the field it wants

    def resolve_links(self, info, **kwargs):
        return Link.objects.all()
#In the snipped above, LinkType was created using the DjangoObjectType - a custom type available in Graphene Django
#Also, the special type query was created with a resolver for the field links, which returns all the links. self= context, **kwargs = args provided to the field in the GraphQL query
# See more about the .objects.... in the django QuerySet Documentation: https://docs.djangoproject.com/en/2.1/ref/models/querysets/#all

#1
class CreateLink(graphene.Mutation):
    id = graphene.Int()
    url = graphene.String()
    description = graphene.String()
    posted_by =graphene.Field(UserType)

    #2   now to define the CreateLink arguments, ie. the data you can send to the server as a client making a create_link mutation request
    class Arguments:
        url = graphene.String()
        description = graphene.String()
    #3
    def mutate(self, info, url, description):
        user = info.context.user or None
        link = Link(url=url, description=description, posted_by=user)  #creates a new link with the passed url and description values
        link.save()  #saves the link

        #available values to return
        return CreateLink(
            id =link.id,
            url=link.url,
            description=link.description,
            posted_by=link.posted_by,
        )
#4
class Mutation(graphene.ObjectType):
    create_link = CreateLink.Field()

#1: Defines a mutation class. Right after, you define the output of the mutation, the data the server can send back to the client.
# The output is defined field by field for learning purposes. In the next mutation you’ll define them as just one.
#2: Defines the data you can send to the server, in this case, the links’ url and description.
#3: The mutation method: it creates a link in the database using the data sent by the user, through the url and description parameters.
# After, the server returns the CreateLink class with the data just created. See how this matches the parameters set on #1.


