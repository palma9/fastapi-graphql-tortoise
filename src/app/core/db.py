from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.core.config import settings

TORTOISE_ORM: dict = {
    "connections": {
        "default": f"postgres://{settings.DB_USER}:{settings.DB_PASSWORD}"
        f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
    },
    "apps": {
        "models": {
            "models": ["app.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


def switch_to_test_mode():
    global TORTOISE_ORM, generate_schemas
    TORTOISE_ORM['connections']['default'] = 'sqlite://:memory:'
    generate_schemas = True


def init_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        db_url=TORTOISE_ORM["connections"]["default"],
        modules={"models": TORTOISE_ORM["apps"]["models"]["models"]},
        generate_schemas=True,
        add_exception_handlers=True,
    )
