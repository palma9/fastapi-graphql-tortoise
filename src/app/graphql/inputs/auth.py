import strawberry


@strawberry.input
class LoginInput:
    email: str = strawberry.argument(description="Email")
    password: str = strawberry.argument(description="Password")


@strawberry.input(description="Register a new user")
class RegisterInput:
    email: str = strawberry.argument(description="Email")
    password: str = strawberry.argument(description="Password")
    first_name: str = strawberry.argument(description="First name")
    last_name: str = strawberry.argument(description="Last name")


@strawberry.input(description="Change your password")
class ChangePasswordInput:
    old_password: str = strawberry.argument(description="Actual password")
    new_password: str = strawberry.argument(description="New password")
