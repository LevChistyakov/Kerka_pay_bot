from tortoise import fields
from tortoise.models import Model


class User(Model):
    id = fields.BigIntField(pk=True)
    telegram_id = fields.BigIntField()
    balance = fields.FloatField(default=0)


class BannedUser(Model):
    id = fields.BigIntField(pk=True)
    telegram_id = fields.BigIntField(unique=True)
