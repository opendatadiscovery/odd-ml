from typing import List, Optional

from prettytable import PrettyTable
from pydantic import BaseModel


class SearchFilterState(BaseModel):
    entityId: int
    entityName: Optional[str]
    selected: bool


class SearchFormDataFilters(BaseModel):
    types: Optional[List[SearchFilterState]]
    subtypes: Optional[List[SearchFilterState]]
    tags: Optional[List[SearchFilterState]]
    namespaces: Optional[List[SearchFilterState]]
    ownes: Optional[List[SearchFilterState]]
    datasources: Optional[List[SearchFilterState]]


class SearchFormData(BaseModel):
    query: Optional[str]
    myObjects: Optional[str]
    filters: SearchFormDataFilters


class SearchApiSearchRequest(BaseModel):
    search_form_data: SearchFormData


class SearchResultItem(BaseModel):
    id: int
    oddrn: str
    external_name: str


class SearchResult(BaseModel):
    items: List[SearchResultItem]

    def show_table(self):
        tbl = PrettyTable()
        tbl.align = "r"
        tbl.field_names = ["Id", "Name", "Oddrn"]
        tbl.add_rows([[i.id, i.external_name, i.oddrn] for i in self.items])
        print(tbl)
