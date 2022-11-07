import strawberry
from strawberry.fastapi import GraphQLRouter

from app.graphql.context import get_context
from app.graphql.mutations.auth import Mutation as AuthMutation
from app.graphql.queries.users import Query as UserQuery
from app.graphql.subscriptions.users import Subscription as UserSubscription

broadcast = None


@strawberry.type
class Query(UserQuery):
    pass


@strawberry.type
class Mutation(AuthMutation):
    pass


class Subscription(UserSubscription):
    pass


schema = strawberry.Schema(query=Query, mutation=Mutation, subscription=Subscription)

graphql_app = GraphQLRouter(schema, context_getter=get_context)
