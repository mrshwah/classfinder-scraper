import graphene

import courses.schema


class Query(courses.schema.Query, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)