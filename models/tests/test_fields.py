# test_fields.py
import pytest
from models.fields import Field, IntegerField, StringField, RelatedField


def test_field_default_value():
    field = Field(default="default_value")
    assert field.get_default() == "default_value"


def test_field_validate():
    field = Field()
    assert field.validate("value")
    assert field.validate(None)
    assert field.validate(42)


def test_integer_field_validate():
    int_field = IntegerField()
    assert int_field.validate(42)
    assert not int_field.validate("42")


def test_string_field_validate():
    str_field = StringField()
    assert str_field.validate("string")
    assert not str_field.validate(42)


def test_related_field_model():
    related_field = RelatedField(model="SomeModel")
    assert related_field.model == "SomeModel"


def test_related_field_inherits_string_field():
    related_field = RelatedField()
    assert related_field.validate("string")
    assert not related_field.validate(42)
