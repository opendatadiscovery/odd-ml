import datetime
from typing import Any, List, Optional

from pydantic import BaseModel, Field

from odd_ml.helpers.asci_renderer import show_table
from .data_source import DataSource


class Field(BaseModel):
    id: int
    name: str
    type: Any
    origin: Any


class MetadataFiled(BaseModel):
    field: Field
    value: Any


class EntityClass(BaseModel):
    id: int
    name: str


class Relative(BaseModel):
    id: int
    entity_classes: List[EntityClass]
    internal_name: Optional[str]
    external_name: str

    @property
    def name(self):
        return self.internal_name or self.external_name

    @property
    def entity_classes_joined(self) -> str:
        return ", ".join([ec.name for ec in self.entity_classes])


class Owner(BaseModel):
    id: int
    name: str


class Role(BaseModel):
    id: int
    name: str


class EntityOwner(BaseModel):
    id: int
    owner: Owner
    role: Role


class DataEntityTag(BaseModel):
    id: int
    name: str


class DataEntityType(BaseModel):
    id: int
    name: str


class DataEntityClass(BaseModel):
    id: int
    name: str
    types: List[DataEntityType]


class DataEntity(BaseModel):
    id: int
    oddrn: str
    external_name: str
    internal_name: Optional[str]
    ownership: Optional[List[EntityOwner]] = []
    data_source: DataSource
    entity_classes: List[DataEntityClass]
    type: DataEntityType
    tags: List[DataEntityTag]
    created_at: Optional[datetime.datetime]
    updated_at: Optional[datetime.datetime]
    metadata_field_values: List[MetadataFiled]
    source_list: Optional[List[Relative]] = []
    target_list: Optional[List[Relative]] = []

    @property
    def entity_class_names(self) -> str:
        return [c.name for c in self.entity_classes]

    def show_details(self):
        field_names = ["Field", "Value"]

        rows = [
            ["id", self.id],
            ["name", self.internal_name or self.external_name],
            ["oddrn", self.oddrn],
            ["type", self.type.name],
            ["entity types", ",".join(self.entity_class_names)],
            ["tags", ", ".join(tag.name for tag in self.tags)],
            [
                "owners",
                ", ".join(
                    f"{o.owner.name} [{o.role.name}]" for o in self.ownership or []
                ),
            ],
        ]

        show_table(field_names, rows, "Details")
        self.show_metadata()
        self.show_relatives()

    def show_metadata(self):
        rows = [[v.field.name, v.value] for v in self.metadata_field_values]
        show_table(["Field", "Value"], rows, "Metadata")

    def show_relatives(self):
        field_names = ["Id", "Name", "Class"]

        show_table(field_names, self.__sources_tbl(), "Sources")
        show_table(field_names, self.__targets_tbl(), "Targets")

    def __sources_tbl(self):
        return self.__relative_rows(self.source_list)

    def __targets_tbl(self):
        return self.__relative_rows(self.target_list)

    @staticmethod
    def __relative_rows(data: Optional[List[Relative]]):
        if data is None:
            data = []
        return [[rel.id, rel.name, rel.entity_classes_joined] for rel in data]
