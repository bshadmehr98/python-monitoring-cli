from models.fields import Field


class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        fields = {}

        for attr_name, attr_value in attrs.items():
            if isinstance(attr_value, Field):
                fields[attr_name] = attr_value
                attrs[attr_name] = attr_value.get_default()
        attrs["_fields"] = fields
        return super(ModelMeta, cls).__new__(cls, name, bases, attrs)
