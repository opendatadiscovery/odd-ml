from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

from pydantic import BaseModel

from odd_ml.helpers.asci_renderer import show_table
from odd_ml.utils import datetime_to_str

from .data_entity import DataEntity, EntityClass
from .data_source import DataSource


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
    internal_name: Optional[str]
    entity_classes: List[EntityClass]
    data_source: DataSource
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    @property
    def name(self):
        return self.internal_name or self.external_name

    @property
    def entity_classes_names(self):
        return [ec.name for ec in self.entity_classes]


class DataEntities(BaseModel):
    """Response from ODD platform /search endpoint

    Args:
        items: (list of str) - list of result items
    """

    items: List[SearchResultItem]

    def show_list(self):
        """Show items list as a table"""

        key_value: Dict[str, Callable[[DataEntity], Any]] = {
            "Id": lambda x: x.id,
            "Name": lambda x: x.name,
            "Type": lambda x: ", ".join(x.entity_classes_names),
            "Data source": lambda x: x.data_source.name,
            "Namespace": lambda x: x.data_source.namespace.name
            if x.data_source.namespace
            else "",
            "Created at": lambda x: datetime_to_str(x.created_at),
            "Updated at": lambda x: datetime_to_str(x.updated_at),
        }

        headers = key_value.keys()
        rows = [[key_value[k](i) for k in headers] for i in self.items]

        show_table(headers, rows, "Data entities")
