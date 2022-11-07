import strawberry

from app.graphql.types.user import UserType


@strawberry.type
class AuthType:
    token: str | None = strawberry.field(description="User's token")
    user: UserType = strawberry.field(description="User")
