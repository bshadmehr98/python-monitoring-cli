from models.fields import Field


class ModelMeta(type):
    def __new__(cls, name, bases, dct):
        fields = {}
        related_fields = {}

        for attr_name, attr_value in dct.items():
            if isinstance(attr_value, Field):
                fields[attr_name] = attr_value
                dct[attr_name] = attr_value.get_default()
        dct["_fields"] = fields
        return super(ModelMeta, cls).__new__(cls, name, bases, dct)
