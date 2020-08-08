import graphene

import registration.schema


class Query(registration.schema.Query, graphene.ObjectType):
    pass


class Mutation(registration.schema.Mutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)

