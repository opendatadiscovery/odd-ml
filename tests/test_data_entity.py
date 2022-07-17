import pytest
from odd_ml.helpers.get_s3_path import get_s3_path
from pydantic_factories import ModelFactory

from odd_ml.domain import DataEntity
from odd_ml.domain.data_entity import DataEntityType
from odd_ml.errors import WrongDataEntityTypeError


class DataEntityFactory(ModelFactory):
    __model__ = DataEntity


def test_data_entity_to_dict():
    de: DataEntity = DataEntityFactory.build(type=DataEntityType(id=1, name="test"))

    with pytest.raises(
        WrongDataEntityTypeError,
        match="Entity is not a dataset",
    ):
        get_s3_path(de)
