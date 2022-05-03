from typing import List, Optional

from prettytable import PrettyTable
from pydantic import BaseModel


class SearchFilterState(BaseModel):
    entity_id: int
    entity_name: Optional[str]
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
    my_objects: Optional[str]
    filters: SearchFormDataFilters


class SearchApiSearchRequest(BaseModel):
    search_form_data: SearchFormData


class SearchResultItem(BaseModel):
    id: int
    oddrn: str
    external_name: str


class SearchResult(BaseModel):
    """Response from ODD platform /search endpoint

    Args:
        items: (list of str) - list of result items
    """

    items: List[SearchResultItem]

    def show_table(self):
        """Show items list as a table"""
        tbl = PrettyTable()
        tbl.align = "r"
        tbl.field_names = ["Id", "Name"]
        tbl.add_rows([[i.id, i.external_name] for i in self.items])
        print(tbl)
