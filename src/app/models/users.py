from tortoise import fields

from app.models.base import BaseModel


class User(BaseModel):
    email = fields.CharField(max_length=255, unique=True)
    first_name = fields.CharField(max_length=50)
    last_name = fields.CharField(max_length=50)
    password = fields.CharField(max_length=128, null=True)
    last_login = fields.DatetimeField(null=True)
    is_active = fields.BooleanField(default=True)
    is_superuser = fields.BooleanField(default=False)

    height = fields.FloatField(null=True)
    weight = fields.FloatField(null=True)
    training_since = fields.DateField(null=True)

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"
