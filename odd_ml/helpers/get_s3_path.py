from odd_ml.domain.data_entity import DataEntity
from odd_ml.errors import WrongDataEntityTypeError
from odd_ml.helpers import oddrn_to_s3_path


def get_s3_path(data_entity: DataEntity) -> str:
    if "DATA_SET" not in data_entity.entity_class_names:
        raise WrongDataEntityTypeError

    return oddrn_to_s3_path(data_entity.oddrn)
