from dataclasses import dataclass
from functools import wraps
import json
from typing import Optional, Type, TypeVar
from pydantic import BaseModel

import requests
from odd_ml.domain.data_entity import DataEntity
from odd_ml.domain.data_source import GetDataSourcesResult

from odd_ml.domain.data_entities import (
    SearchFilterState,
    SearchFormData,
    SearchFormDataFilters,
    DataEntities,
)

T = TypeVar("T", bound=BaseModel)


@dataclass
class SearchConfig:
    data_source_id: Optional[int] = None
    query: Optional[str] = ""
    page: int = 1
    size: int = 30


def map_response_to(mapper: Type[T]):
    def inner(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            return mapper.parse_raw(func(*args, **kwargs))

        return wrapped

    return inner


class HttpClient:
    def __init__(self, platform_url: str) -> None:
        self.__url = platform_url

    @map_response_to(DataEntities)
    def search(self, search_config: SearchConfig) -> DataEntities:
        """Search any data entity

        Args:
            query (str): searching text
            datasource_id (int, optional): datasource id for narrowing search. Defaults to None.

        Returns:
            SearchResult
        """
        search_id = self.__get_search_id(search_config)
        url = f"{self.__url}/api/search/{search_id}/results?page={search_config.page}&size={search_config.size}"
        return self.__get(url)

    @map_response_to(GetDataSourcesResult)
    def get_data_sources(self, page: int = 1, size: int = 100) -> GetDataSourcesResult:
        """List of all DataSources

        Returns:
            GetDataSourcesResult
        """
        return self.__get(f"{self.__url}/api/datasources?page={page}&size={size}")

    @map_response_to(DataEntity)
    def get_data_entity_by_id(self, id: int) -> DataEntity:
        """Getting data entity id

        Args:
            id (int): id of data entity

        Returns:
            DataEntity
        """

        return self.__get(f"{self.__url}/api/dataentities/{id}")

    def __get_search_id(self, search_config: SearchConfig) -> str:
        """Each search request needs hashed search id from platform

            str: if successfully, else raises HTTPError

        Raises:
            HTTPError: in case of server returned error
        """
        filters = SearchFormDataFilters()

        # TODO: Add more filter
        if search_config.data_source_id:
            filters.datasources = [
                SearchFilterState(entity_id=search_config.data_source_id, selected=True)
            ]

        data = SearchFormData(
            query=search_config.query,
            filters=filters,
        )

        res = requests.post(
            url=f"{self.__url}/api/search",
            data=data.json(),
            headers={"Content-Type": "application/json"},
        )
        res.raise_for_status()

        return json.loads(res.text).get("search_id")

    @staticmethod
    def __get(url) -> str:
        res = requests.get(url)
        res.raise_for_status()
        return res.text
