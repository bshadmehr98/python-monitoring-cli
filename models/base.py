import os
import json

from models.meta import ModelMeta
from models.fields import Field, StringField, IntegerField
from models.queryset import QuerySet


class Model(metaclass=ModelMeta):
    _instances = []

    def __init__(self, **kwargs):
        for field_name, field_value in kwargs.items():
            if field_name in self._fields and self._fields[field_name].validate(
                field_value
            ):
                self._fields[field_name].value = field_value
                setattr(self, field_name, field_value)
            else:
                raise ValueError(f"Invalid value for field '{field_name}'")

    @classmethod
    def _get_data_file(cls):
        try:
            os.makedirs(f"./.data/{cls.__name__}")
        except FileExistsError:
            # directory already exists
            pass
        if not os.path.exists(f"./.data/{cls.__name__}/data.json"):
            with open(f"./.data/{cls.__name__}/data.json", 'w'): pass
        return f"./.data/{cls.__name__}/data.json"

    @classmethod
    def load_data(cls):
        with open(cls._get_data_file(), "r") as f:
            content = f.read()
            if not content:
                return []
            return json.loads(content)

    @classmethod
    def save_data(cls, data):
        # TODO: Add a safety mechanism, like a cache and safe apply
        data_file = cls._get_data_file()
        with open(data_file, "w") as f:
            json.dump(data, f, indent=2)

    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        data = cls.load_data()
        data.append(instance.__dict__)
        cls.save_data(data)
        return instance

    @classmethod
    def all(cls):
        data = cls.load_data()
        return QuerySet(cls, data)

    def save(self):
        data = self.load_data()
        for i, instance_data in enumerate(data):
            if instance_data["id"] == self.id:
                data[i] = self.__dict__
                break
        else:
            self.id = len(data) + 1
            data.append(self.__dict__)
        self.save_data(data)

    def delete(self):
        data = self.all().all()
        data = [item.__dict__ for item in data if item.id != self.id]
        self.save_data(data)

    @classmethod
    def query(cls, **kwargs):
        data = cls.load_data()
        filtered_data = [
            d for d in data if all(d.get(key) == value for key, value in kwargs.items())
        ]
        return QuerySet(cls, filtered_data)
