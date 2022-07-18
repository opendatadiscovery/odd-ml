from ast import Dict
from pprint import pprint
from typing import Any, Callable, List, Optional

from prettytable import PrettyTable
from pydantic import BaseModel
from odd_ml.domain.namespace import Namespace

from odd_ml.helpers.asci_renderer import show_table


class DataSource(BaseModel):
    id: int
    oddrn: str
    name: str
    namespace: Optional[Namespace]
    description: Optional[str]
    connection_url: Optional[str]
    active: bool

    def show_details(self):
        tbl = PrettyTable()
        tbl.align = "l"
        tbl.field_names = ["Key", "Value"]
        tbl.add_rows(self.dict().items())
        pprint(tbl)


class GetDataSourcesResult(BaseModel):
    items: List[DataSource]

    def get_data_source_by(self, data_source_id: int):
        ds = next((x for x in self.items if x.id == data_source_id), None)

        if not ds:
            raise ValueError(f"Datasource with id {data_source_id}  was not found")

        return ds

    def show_table(self):
        key_value: Dict[str, Callable[[Any], Any]] = {
            "Id": lambda x: x.id,
            "Name": lambda x: x.name,
            "Oddrn": lambda x: x.oddrn,
        }

        headers = key_value.keys()
        rows = [[key_value[header](item) for header in headers] for item in self.items]

        show_table(headers, rows, title="Data sources")
