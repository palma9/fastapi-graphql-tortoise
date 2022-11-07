import strawberry
from graphql import GraphQLError
from strawberry.types import Info

from app.core.auth import IsAuthenticated
from app.graphql.types.user import UserType
from app.models.users import User


@strawberry.type
class Query:

    @strawberry.field(
        description="Get a list of all users",
        permission_classes=[IsAuthenticated]
    )
    async def users(self) -> list[UserType]:
        """Get all users"""
        return await User.all()

    @strawberry.field(description="Get a single user by id")
    async def user(self, user_id: str) -> UserType:
        """Get one user"""
        try:
            return await User.get(id=user_id)

        except Exception as error:
            raise GraphQLError(error)

    @strawberry.field(description="Get authenticated user")
    async def me(self, info: Info) -> UserType:
        """Get authenticated user"""
        return info.context['user']
