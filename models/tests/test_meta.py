# test_model_meta.py
import pytest
from models.fields import Field
from models.meta import ModelMeta

class StringField(Field):
    pass

class IntegerField(Field):
    pass

class TestModel(metaclass=ModelMeta):
    name = StringField(default="")
    age = IntegerField(default=0)

def test_model_meta_fields_initialized():
    assert hasattr(TestModel, "_fields")
    assert isinstance(TestModel._fields, dict)
    assert "name" in TestModel._fields
    assert "age" in TestModel._fields

def test_model_meta_default_values():
    assert hasattr(TestModel, "name")
    assert hasattr(TestModel, "age")
    assert isinstance(TestModel._fields["name"], StringField)
    assert isinstance(TestModel._fields["age"], IntegerField)
    assert isinstance(TestModel.name, str)
    assert isinstance(TestModel.age, int)

def test_model_meta_default_values_after_instantiation():
    instance = TestModel()
    assert instance.name == ""
    assert instance.age == 0
