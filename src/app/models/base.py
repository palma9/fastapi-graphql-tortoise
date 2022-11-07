from datetime import datetime
from uuid import UUID

from tortoise import fields, models


class BaseModel(models.Model):
    id: UUID = fields.UUIDField(pk=True, index=True)
    created: datetime = fields.DatetimeField(auto_now_add=True)
    modified: datetime = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True
