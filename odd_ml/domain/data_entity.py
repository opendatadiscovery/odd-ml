from typing import Any, List, Optional

from prettytable import PrettyTable
from pydantic import BaseModel


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
    data_entity_id: int


class DataEntity(BaseModel):
    id: int
    oddrn: str
    external_name: str
    metadata_field_values: List[MetadataFiled]
    source_list: Optional[List[Relative]] = []
    target_list: Optional[List[Relative]] = []
    ownership: List[EntityOwner] = []

    def show_owners(self):
        tbl = PrettyTable()
        tbl.field_names = ["Name", "Role"]
        tbl.align = "l"

        rows = [[o.owner.name, o.role.name] for o in self.ownership]

        tbl.add_rows(rows)
        print(tbl)

    def show_metadata(self):
        tbl = PrettyTable()
        tbl.field_names = ["Name", "Value"]
        tbl.align = "l"

        rows = [[v.field.name, v.value] for v in self.metadata_field_values]

        tbl.add_rows(rows)
        print(tbl)

    def show_relatives(self):
        print("Sources")
        print(self.__sources_tbl())

        print("Targets")
        print(self.__targets_tbl())

    def __sources_tbl(self):
        tbl = PrettyTable()
        return self.__relative_table(self.source_list, tbl)

    def __targets_tbl(self):
        tbl = PrettyTable()
        return self.__relative_table(self.target_list, tbl)

    @staticmethod
    def __relative_table(data: List[Relative], tbl: PrettyTable = None):
        if tbl is None:
            tbl = PrettyTable()

        tbl.field_names = ["Id", "Name", "Class"]
        rows = [[rel.id, rel.name, rel.entity_classes_joined] for rel in data]

        tbl.add_rows(rows)

        return tbl
