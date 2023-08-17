from models.base import Model, StringField, IntegerField


class URLModel(Model):
    id = StringField()
    address = StringField()
    port = IntegerField(default=0)
    protocol = StringField()
    interval = IntegerField(default=1)

    def __repr__(self):
        return f"URL(address='{self.address}', port={self.port})"
