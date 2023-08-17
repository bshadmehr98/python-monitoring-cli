from models.base import Model
from models.fields import StringField, IntegerField, RelatedField
from models.channel import ChannelModel
from models.url import URLModel


class HistoryModel(Model):
    id = StringField()
    endpoint = RelatedField(model=URLModel)
    status = IntegerField()
    ok = IntegerField()
    ts = IntegerField()
    date = StringField()

    def __repr__(self):
        return f"History(id='{self.id}', url={self.endpoint}, status={self.status})"
