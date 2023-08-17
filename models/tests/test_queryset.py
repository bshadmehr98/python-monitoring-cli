# test_queryset.py
import pytest
from models.fields import Field, RelatedField
from models.queryset import QuerySet
from models.meta import ModelMeta

class SampleModel(metaclass=ModelMeta):
    def __init__(self, **kwargs):
        for field_name, field_value in kwargs.items():
            if field_name in self._fields and self._fields[field_name].validate(
                field_value
            ):
                self._fields[field_name].value = field_value
                setattr(self, field_name, field_value)
            else:
                raise ValueError(f"Invalid value for field '{field_name}'")

    id = Field()
    name = Field()
    age = Field()
    related_id = RelatedField(model=SampleModel)

def test_queryset_filter():
    data = [
        {"id": 1, "name": "Alice", "age": 25, "related_id": "1"},
        {"id": 2, "name": "Bob", "age": 30, "related_id": "2"},
        {"id": 3, "name": "Charlie", "age": 22, "related_id": "1"},
    ]
    queryset = QuerySet(SampleModel, data)

    filtered_queryset = queryset.filter(name="Alice", age=25)
    assert len(filtered_queryset.all()) == 1
    assert filtered_queryset.all()[0].name == "Alice"

def test_queryset_filter_related():
    data = [
        {"id": 1, "name": "Alice", "age": 25, "related_id": "1"},
        {"id": 2, "name": "Bob", "age": 30, "related_id": "2"},
        {"id": 3, "name": "Charlie", "age": 22, "related_id": "1"},
    ]
    queryset = QuerySet(SampleModel, data)

    filtered_queryset = queryset.filter(related_id="2")
    assert len(filtered_queryset.all()) == 1
    assert filtered_queryset.all()[0].name == "Bob"

def test_queryset_map():
    data = [
        {"id": 1, "name": "Alice", "age": 25, "related_id": "1"},
        {"id": 2, "name": "Bob", "age": 30, "related_id": "2"},
        {"id": 3, "name": "Charlie", "age": 22, "related_id": "1"},
    ]
    queryset = QuerySet(SampleModel, data)

    mapped_data = queryset.map(lambda instance: instance.name.upper())
    assert mapped_data == ["ALICE", "BOB", "CHARLIE"]

def test_queryset_load_related():
    data = [
        {"id": 1, "name": "Alice", "age": 25, "related_id": "1"},
        {"id": 2, "name": "Bob", "age": 30, "related_id": "2"},
    ]
    related_data = [
        {"id": 1, "name": "Related1"},
        {"id": 2, "name": "Related2"},
    ]
    related_queryset = QuerySet(SampleModel, related_data)
    queryset = QuerySet(SampleModel, data)

    queryset.load_related()
    assert hasattr(queryset.all()[0], "related_id_obj")
    assert queryset.all()[0].related_id_obj.name == "Related1"

def test_queryset_get():
    data = [
        {"id": 1, "name": "Alice", "age": 25, "related_id": "1"},
        {"id": 2, "name": "Bob", "age": 30, "related_id": "2"},
    ]
    queryset = QuerySet(SampleModel, data)

    instance = queryset.get(name="Alice")
    assert instance.name == "Alice"

def test_queryset_get_no_record():
    data = []
    queryset = QuerySet(SampleModel, data)

    with pytest.raises(Exception, match="No record found"):
        queryset.get(name="Alice")

def test_queryset_get_multiple_records():
    data = [
        {"id": 1, "name": "Alice", "age": 25, "related_id": "1"},
        {"id": 2, "name": "Alice", "age": 30, "related_id": "2"},
    ]
    queryset = QuerySet(SampleModel, data)

    with pytest.raises(Exception, match="More than 1 record found"):
        queryset.get(name="Alice")
