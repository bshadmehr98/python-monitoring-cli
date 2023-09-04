import pytest
from unittest.mock import patch

from models.queryset import QuerySet
from models.meta import ModelMeta
from models.fields import StringField, IntegerField, RelatedField


class SampleRelatedModel(metaclass=ModelMeta):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    role = StringField()


class SampleModel(metaclass=ModelMeta):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    name = StringField()
    age = IntegerField()
    role = RelatedField(model=SampleRelatedModel)


def test_queryset_filter():
    data = [
        {"name": "Alice", "age": 25},
        {"name": "Bob", "age": 30},
        {"name": "Charlie", "age": 28},
    ]
    queryset = QuerySet(SampleModel, data)

    # Filter by age
    filtered_queryset = queryset.filter(age=30)
    assert len(filtered_queryset.all()) == 1
    assert filtered_queryset.all()[0].name == "Bob"

    # Filter by name
    filtered_queryset = queryset.filter(name="Alice")
    assert len(filtered_queryset.all()) == 1
    assert filtered_queryset.all()[0].age == 25


def test_queryset_get():
    # Test the get method
    data = [
        {"name": "Alice", "age": 25},
        {"name": "Alice", "age": 28},
        {"name": "Bob", "age": 30},
    ]
    queryset = QuerySet(SampleModel, data)

    # Get a single instance
    instance = queryset.get(age=30)
    assert instance.name == "Bob"

    # Multiple records found should raise an exception
    with pytest.raises(Exception, match="More than 1 record found"):
        queryset.get(name="Alice")

    # No records found should raise an exception
    with pytest.raises(Exception, match="No record found"):
        queryset.get(name="Eve")


def test_queryset_map():
    # Test the map method
    data = [
        {"name": "Alice", "age": 25},
        {"name": "Bob", "age": 30},
    ]
    queryset = QuerySet(SampleModel, data)

    # Define a mapping function
    def custom_mapping(instance):
        return f"{instance.name} is {instance.age} years old"

    # Apply the mapping function to the queryset
    mapped_results = queryset.map(custom_mapping)

    # Check the mapped results
    assert len(mapped_results) == 2
    assert mapped_results[0] == "Alice is 25 years old"
    assert mapped_results[1] == "Bob is 30 years old"


def test_queryset_load_related():
    # Test the load_related method
    data = [
        {"name": "Alice", "age": 25, "role": "1"},
        {"name": "Bob", "age": 30, "role": "2"},
    ]

    # Create instances with related IDs
    queryset = QuerySet(SampleModel, data)

    # Create related instances data
    related_data = [
        {"role": "Admin", "id": "1"},
        {"role": "User", "id": "2"},
    ]

    # Create a new queryset for the related instances
    related_queryset = QuerySet(SampleRelatedModel, related_data)

    # Replace the RelatedField model's all() method with the related queryset
    SampleModel._fields["role"].model.all = lambda: related_queryset

    # Load related objects
    queryset.load_related()

    # Check if related objects are loaded correctly
    assert hasattr(queryset.all()[0], "role_obj")
    assert queryset.all()[0].role_obj.role == "Admin"
    assert hasattr(queryset.all()[1], "role_obj")
    assert queryset.all()[1].role_obj.role == "User"
