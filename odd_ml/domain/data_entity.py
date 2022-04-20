from typing import Any, List

from pydantic import BaseModel


class Field(BaseModel):
    id: int
    name: str
    type: Any
    origin: Any


class MetadataFiled(BaseModel):
    field: Field
    value: Any


class DataEntity(BaseModel):
    id: int
    oddrn: str
    external_name: str
    metadata_field_values: List[MetadataFiled]
