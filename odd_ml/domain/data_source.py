from typing import List

from prettytable import PrettyTable
from pydantic import BaseModel


class DataSource(BaseModel):
    id: int
    oddrn: str
    name: str


class GetDataSourcesResult(BaseModel):
    items: List[DataSource]

    def show_table(self):
        tbl = PrettyTable()
        tbl.align = "r"
        tbl.field_names = ["Id", "Name", "Oddrn"]
        tbl.add_rows([[i.id, i.name, i.oddrn] for i in self.items])
        print(tbl)
