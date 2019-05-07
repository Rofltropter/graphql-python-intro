import graphene

import links.schema
# ^not sure about this one, a little tricky.
import users.schema

#defining the Query. This inherits the query defined before, so we can keep every part of the schema isolated in the apps!
class Query(
    links.schema.Query,
    users.schema.Query,
    graphene.ObjectType
):
    pass
# pass is used when a statement it required syntactically, but you do not want to execute any code

class Mutation(
    users.schema.Mutation,
    links.schema.Mutation,
    graphene.ObjectType
):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)