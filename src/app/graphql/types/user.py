from datetime import date
from uuid import UUID

import strawberry


@strawberry.type
class UserType:
    id: UUID = strawberry.field(description="User's id")
    email: str = strawberry.field(description="User's email")
    first_name: str = strawberry.field(description="First name")
    last_name: str = strawberry.field(description="Last name")
    full_name: str = strawberry.field(description="Full name")
    height: float | None = strawberry.field(description="Height")
    weight: float | None = strawberry.field(description="Weight")
    training_since: date | None = strawberry.field(
        description="Training since"
    )
