import asyncio
from typing import Iterator
from uuid import UUID

import pytest
from fastapi.testclient import TestClient
from tortoise.contrib.test import finalizer, initializer

from app.core.db import TORTOISE_ORM, switch_to_test_mode
from app.models import User

switch_to_test_mode()

ADMIN_EMAIL: str = "admin@admin.com"


@pytest.fixture(scope="module")
def event_loop() -> Iterator[asyncio.AbstractEventLoop]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="module")
def client(event_loop: asyncio.BaseEventLoop) -> Iterator[TestClient]:
    from main import app

    initializer(TORTOISE_ORM["apps"]["models"]["models"], loop=event_loop)
    with TestClient(app) as c:
        yield c
    finalizer()


def test_create_user(client: TestClient, event_loop: asyncio.AbstractEventLoop) -> None:
    data: dict = {
        "email": ADMIN_EMAIL,
        "password": "test",
        "first_name": "test",
        "last_name": "test"
    }

    query = User.create(**data)
    user: User = event_loop.run_until_complete(query)

    assert user.email == data["email"]
    assert user.first_name == data["first_name"]
    assert user.last_name == data["last_name"]
    assert user.is_active is True
    assert user.is_superuser is False
    assert type(user.id) == UUID


def test_get_user(client: TestClient, event_loop: asyncio.AbstractEventLoop) -> None:
    query = User.get_or_none(email=ADMIN_EMAIL)
    user: User = event_loop.run_until_complete(query)

    assert user is not None
    assert user.email == ADMIN_EMAIL
    assert user.is_active is True
    assert user.is_superuser is False
    assert type(user.id) == UUID


def test_update_user(client: TestClient, event_loop: asyncio.AbstractEventLoop) -> None:
    new_first_name: str = "new_first_name"
    new_last_name: str = "new_last_name"

    query = User.filter(email=ADMIN_EMAIL).update(
        first_name=new_first_name, last_name=new_last_name
    )

    event_loop.run_until_complete(query)

    get_user = User.get_or_none(email=ADMIN_EMAIL)
    user: User = event_loop.run_until_complete(get_user)

    assert user is not None
    assert user.email == ADMIN_EMAIL
    assert user.first_name == new_first_name
    assert user.last_name == new_last_name
    assert user.is_active is True
    assert user.is_superuser is False
    assert type(user.id) == UUID


def test_delete_user(client: TestClient, event_loop: asyncio.AbstractEventLoop) -> None:
    query = User.filter(email=ADMIN_EMAIL).delete()
    event_loop.run_until_complete(query)

    get_user = User.get_or_none(email=ADMIN_EMAIL)
    user: User = event_loop.run_until_complete(get_user)

    assert user is None
