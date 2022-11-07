from broadcaster import Broadcast

from app.core.config import settings

broadcast = None


async def init_broadcast():
    global broadcast

    if not broadcast:
        broadcast = Broadcast(settings.BROADCAST_URL)
        await broadcast.connect()

    return broadcast


async def get_context():
    return {"broadcast": await init_broadcast()}
