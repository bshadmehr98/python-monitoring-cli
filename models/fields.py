class Field:
    def __init__(self, value=None, default=None):
        self.default = default
        self.value = value

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
    def __init__(self, model=None, default=None):
        self.default = default
        self.model = model
