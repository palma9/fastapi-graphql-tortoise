from redis import Redis

from app.core.config import settings

conn = Redis(settings.REDIS_HOST)


def set_value(key: str, value: str, expire: int = 300) -> None:
    """Set a value in the redis database
    Args:
        key (str): Key to set in the redis database
        value (str): Value to set in the redis database
        expire (int, optional): Expiration time in seconds. Defaults to 300.
    """
    conn.set(key, value, expire)


def get_value(key: str) -> bytes | None:
    """Get value from redis database
    Args:
        key (str): Key to get from the redis database
    Returns:
        Optional[bytes]: Value from the redis database
    """
    return conn.get(key)


def get_value_and_delete(key: str) -> bytes | None:
    """Get value from redis database and delete it
    Args:
        key (str): Key to get from the redis database
    Returns:
        Optional[bytes]: Value from the redis database
    """
    return conn.getdel(key)


def exists(key: str) -> bool:
    """Check if a key exists in the redis database
    Args:
        key (str): Key to check in the redis database
    Returns:
        bool: True if key exists, False otherwise
    """
    return conn.exists(key)
