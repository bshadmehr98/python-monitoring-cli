import os
import pytest
import json
import tempfile

from unittest.mock import patch, MagicMock
from models.fields import IntegerField, StringField
from models.base import Model


@pytest.fixture
def temporary_json_file():
    data = [{"name": "Bahman", "age": 4}, {"name": "Ali", "age": 3}]
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
        json.dump(data, temp_file)
        temp_file.flush()
        yield temp_file.name
        temp_file.close()


class SampleModel(Model):
    id = StringField()
    name = StringField()
    age = IntegerField()


def test_init():
    instance = SampleModel(id="1", name="Test", age=30)
    assert hasattr(instance, "id")
    assert hasattr(instance, "name")
    assert hasattr(instance, "age")

    assert instance.id == "1"
    assert instance.name == "Test"
    assert instance.age == 30


def test_validate_called():
    with patch.object(IntegerField, "validate", return_value=True) as int_validate_mock:
        instance = SampleModel(id="1", name="Test", age=30)

        assert int_validate_mock.call_count == 1

    with patch.object(StringField, "validate", return_value=True) as str_validate_mock:
        instance = SampleModel(id="1", name="Test", age=30)

        assert str_validate_mock.call_count == 2


def test_data_file_path():
    final = os.path.normpath(SampleModel._get_data_file())
    expecetd = os.path.normpath("./.data/SampleModel/data.json")
    assert final == expecetd


def test_load_data(temporary_json_file):
    with patch.object(SampleModel, "_get_data_file", return_value=temporary_json_file):
        loaded_data = SampleModel.load_data()
        expected_data = [{"name": "Bahman", "age": 4}, {"name": "Ali", "age": 3}]
        assert loaded_data == expected_data


def test_save_data(temporary_json_file):
    with patch.object(SampleModel, "_get_data_file", return_value=temporary_json_file):
        data_to_save = [{"name": "Zahra", "age": 2}, {"name": "Fateme", "age": 5}]
        SampleModel.save_data(data_to_save)

        with open(temporary_json_file, "r") as f:
            saved_data = json.load(f)

        assert saved_data == data_to_save


def test_create():
    data = []

    with patch.object(Model, "load_data", return_value=data):
        with patch.object(Model, "save_data", return_value=None) as save_data:
           instance = SampleModel.create(name="Test", age=25)
           save_data.assert_called_once_with([{'name': 'Test', 'age': 25}])

    assert instance.name == "Test"
    assert instance.age == 25


def test_save():
    data = [{"id": "1", "name": "Existing"}]

    with patch.object(Model, "load_data", return_value=data):
        instance = SampleModel(id="1", name="Updated")
        with patch.object(Model, "save_data", return_value=None) as save_data:
            instance.save()
            save_data.assert_called_once_with([{"id": "1", "name": "Updated"}])

            assert instance.name == "Updated"


def test_delete():
    data = [{"id": "1", "name": "Existing"}, {"id": "2", "name": "To be deleted"}]

    with patch.object(Model, "load_data", return_value=data):
        instance = SampleModel(id="2", name="To be deleted")

        with patch.object(Model, "save_data", return_value=None) as save_data:
            instance.delete()
            save_data.assert_called_once_with([{"id": "1", "name": "Existing"}])


def test_all():
    data = [{"id": "1", "name": "Test1"}, {"id": "2", "name": "Test2"}]

    with patch.object(Model, "load_data", return_value=data):
        res = SampleModel.all().all()

    assert len(res) == 2
    assert res[0].name == "Test1"
    assert res[1].name == "Test2"


def test_query():
    data = [{"id": "1", "name": "Test1"}, {"id": "2", "name": "Test2"}]

    with patch.object(Model, "load_data", return_value=data):
        queryset = SampleModel.query(name="Test1").all()

    assert len(queryset) == 1
    assert queryset[0].name == "Test1"
