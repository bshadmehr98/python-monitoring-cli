from enum import IntEnum

from models.base import Model, StringField, IntegerField


class ChannelType(IntEnum):
    SLACK = 1


class ChannelModel(Model):
    id = StringField()
    type = IntegerField()
    webhook_url = StringField()

    def __repr__(self):
        return f"URL(type='{self.type}', webhook_url={self.webhook_url})"

    @property
    def type_value(self):
        if self.type == ChannelType.SLACK:
            return "slack"
