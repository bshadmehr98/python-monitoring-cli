import pytest
from models.fields import Field
from models.meta import ModelMeta


class SampleModel(metaclass=ModelMeta):
    name = Field()
    age = Field(default=30)
    email = Field(default="example@example.com")


# Define test cases
def test_model_meta_fields():
    # Check if the class attribute _fields is correctly populated
    assert hasattr(SampleModel, "_fields")
    assert isinstance(SampleModel._fields, dict)
    assert "name" in SampleModel._fields
    assert "age" in SampleModel._fields
    assert "email" in SampleModel._fields


def test_model_meta_default_values():
    assert (
        SampleModel._fields["name"].get_default() == None
    )  # Assuming Field default is None
    assert SampleModel._fields["age"].get_default() == 30
    assert SampleModel._fields["email"].get_default() == "example@example.com"


def test_model_meta_instantiation():
    instance = SampleModel()
    assert instance.name == None  # Assuming Field default is None
    assert instance.age == 30
    assert instance.email == "example@example.com"
