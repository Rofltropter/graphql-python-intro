import graphene
import graphql_jwt

import links.schema
# ^not sure about this one, a little tricky.
import users.schema

import links.schema_relay


#defining the Query. This inherits the query defined before, so we can keep every part of the schema isolated in the apps!
class Query(
    links.schema.Query,
    users.schema.Query,
    links.schema_relay.RelayQuery,
    graphene.ObjectType,
):
    pass
# pass is used when a statement it required syntactically, but you do not want to execute any code

class Mutation(
    users.schema.Mutation,
    links.schema.Mutation,
    links.schema_relay.RelayMutation,
    graphene.ObjectType):
    #now moving onto the definitions
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    #The library creates 3 mutations for us
    #tokenAuth is used to authenticate the User with its username and password to obtain the JSON web token
    #verifyToken verifies that the token is valid, passing it as an argument
    #refreshToken obtains a new token within the renewed expiration time for non-expired tokens(if they are able to expire)

schema = graphene.Schema(query=Query, mutation=Mutation)