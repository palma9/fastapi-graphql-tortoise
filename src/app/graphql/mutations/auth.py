import strawberry
from strawberry.types import Info

from app.core.auth import (
    IsAuthenticated,
    encode_token,
    hash_password,
    social_auth,
    verify_password,
)
from app.graphql.inputs.auth import ChangePasswordInput, LoginInput, RegisterInput
from app.graphql.types.auth import AuthType
from app.models import User
from tortoise.expressions import F


@strawberry.type
class Mutation:

    @strawberry.mutation(description="Register a new user")
    async def register(self, info: Info, data: RegisterInput) -> AuthType:
        data_dict: dict = data.__dict__
        data_dict['password'] = hash_password(data_dict['password'])

        if await User.filter(email=data_dict['email']).exists():
            raise ValueError('User already exists')

        print(await User.filter(email=data_dict['email']).annotate(full_name=F("first_name") + " " + F("last_name")).full_name)
        user: User = await User.create(**data_dict)
        info.context["background_tasks"].add_task(info.context["broadcast"].publish, "users", str(user.id))

        return AuthType(
            token=encode_token(user.id),
            user=user
        )

    @strawberry.mutation(description='Login user')
    async def login(self, data: LoginInput) -> AuthType:
        data_dict: dict = data.__dict__

        user = await User.filter(email=data_dict['email']).first()

        if user and verify_password(data_dict['password'], user.password):
            return AuthType(token=encode_token(user.id), user=user)

        raise ValueError('Invalid credentials')

    @strawberry.mutation(description="Login with Google or Apple account")
    async def social_login(self, provider: str, access_token: str) -> AuthType:
        auth_data: dict = social_auth(provider, access_token)

        email = auth_data.pop('email')
        user, _ = await User.get_or_create(email=email, defaults=auth_data)

        return AuthType(token=encode_token(user.id), user=user)

    @strawberry.mutation(
        description="Change your password",
        permission_classes=[IsAuthenticated]
    )
    async def change_password(
        self, info: Info, data: ChangePasswordInput
    ) -> bool:
        user: User = info.context["user"]
        if not verify_password(data.old_password, user.password):
            raise ValueError('Invalid credentials')

        user.password = hash_password(data.new_password)
        await user.save()

        return True
