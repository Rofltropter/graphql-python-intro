import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Link, Vote


#Relay allows the use of django-filter for data filtering. this FilterSet contains the url and description fields. This is a short example of what Relay implementation looks like
class LinkFilter(django_filters.FilterSet):
    class Meta:
        model = Link
        fields = ['url', 'description']

#
class LinkNode(DjangoObjectType):
    class Meta:
        model = Link

        #Data is exposed in nodes, so we create one for the links. Each node implements an interface with a unique ID.
        interfaces = (
            graphene.relay.Node,
        )

class VoteNode(DjangoObjectType):
    class Meta:
        model = Vote
        interfaces = (
            graphene.relay.Node,
        )
class RelayQuery(graphene.ObjectType):          #placed into master schema just like other Queries are
    #Uses the LinkNode with the relay_link field inside your new query
    relay_link = graphene.relay.Node.Field(LinkNode)
    #Defines relay_links field as a Connection, which implements the pagination structure
    relay_links = DjangoFilterConnectionField(LinkNode, filterset_class=LinkFilter)


class RelayCreateLink(graphene.relay.ClientIDMutation):
    link = graphene.Field(LinkNode)

    class Input:
        url = graphene.String()
        description= graphene.String()

    def mutate_and_get_payload(root, info, **input):
        user = info.context.user or None

        link = Link(
            url = input.get('url'),
            description = input.get('description'),
            posted_by = user,
        )
        link.save()

        return RelayCreateLink(link=link)

class RelayMutation(graphene.AbstractType):
    relay_create_link = RelayCreateLink.Field()