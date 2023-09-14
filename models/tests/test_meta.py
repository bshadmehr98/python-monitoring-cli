from models.fields import IntegerField, StringField
from models.meta import ModelMeta


class SampleModel(metaclass=ModelMeta):
    name = StringField()
    age = IntegerField(default=30)
    email = StringField(default="example@example.com")


# Define test cases
def test_model_meta_fields():
    assert hasattr(SampleModel, "_fields")
    assert isinstance(SampleModel._fields, dict)
    assert "name" in SampleModel._fields
    assert "age" in SampleModel._fields
    assert "email" in SampleModel._fields


def test_model_meta_default_values():
    assert (
        SampleModel._fields["name"].get_default() == None
    )
    assert SampleModel._fields["age"].get_default() == 30
    assert SampleModel._fields["email"].get_default() == "example@example.com"


def test_model_meta_instantiation():
    instance = SampleModel()
    assert instance.name == None
    assert instance.age == 30
    assert instance.email == "example@example.com"
