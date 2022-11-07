from typing import AsyncGenerator

import strawberry
from strawberry.types import Info


@strawberry.type
class Subscription:
    @strawberry.subscription
    async def users(self, info: Info) -> AsyncGenerator[str, None]:
        async with info.context['broadcast'].subscribe('users') as subscriber:
            async for event in subscriber:
                yield event.message
