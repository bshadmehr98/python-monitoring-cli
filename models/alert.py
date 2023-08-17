from models.base import Model
from models.fields import StringField, IntegerField, RelatedField
from models.channel import ChannelModel
from models.url import URLModel


class AlertModel(Model):
    id = StringField()
    channel = RelatedField(model=ChannelModel)
    endpoint = RelatedField(model=URLModel)
    occurrence = IntegerField()
    status_code = IntegerField()

    def __repr__(self):
        return f"Alert(id='{self.id}', channel={self.channel})"
