class Field:
    def __init__(self, default=None):
        self.default = default

    def get_default(self):
        return self.default

    def validate(self, value):
        return True


class IntegerField(Field):
    def validate(self, value):
        return isinstance(value, int)


class StringField(Field):
    def validate(self, value):
        return isinstance(value, str)


class RelatedField(StringField):
    def __init__(self, default=None, model=None):
        self.model = model
        super(RelatedField, self).__init__(default=default)
