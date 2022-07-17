import logging
from typing import Optional

import pandas as pd

from odd_ml.domain.data_entities import DataEntities, DataEntity
from odd_ml.dataset_storage.dataset_storage import DatasetStorage
from odd_ml.domain.data_source import GetDataSourcesResult
from odd_ml.errors import ProfilerError
from odd_ml.http.http_client import HttpClient, SearchConfig
from odd_ml.profiler import PandasProfiler
from odd_ml.renderer import IFrameRenderer


class Client:
    """Client for retrieving data from odd-platform"""

    def __init__(self, platform_url, storage: Optional[DatasetStorage] = None):
        """Creating client

        Args:
            platform_url (str): url to odd-platform
            storage (DatasetStorage): using for getting dataframe from datasets
        """
        self.__renderer = IFrameRenderer(platform_url)
        self.__storage = storage
        self.__http = HttpClient(platform_url)
        self.__profiler = PandasProfiler()

    # TODO: add more id for filter (i.e: namespace_id: id, ...)
    @property
    def storage(self):
        return self.__storage

    @storage.setter
    def storage(self, storage: DatasetStorage):
        self.__storage = storage

    def get_data_entities(
        self,
        search_config: Optional[SearchConfig] = None,
    ) -> DataEntities:
        """Getting list of data entities

        Args:
            search_config: SearchConfig
        Returns:
            SearchResult
        """
        if search_config is None:
            search_config = SearchConfig()

        return self.__http.search(search_config)

    def get_data_sources(self, page: int = 1, size: int = 100) -> GetDataSourcesResult:
        """List of DataSources

        Returns:
            GetDataSourcesResult
        """
        return self.__http.get_data_sources(page, size)

    def get_data_entity_by_id(self, id: int) -> DataEntity:
        """Getting data entity id

        Args:
            id (int): id of data entity

        Returns:
            DataEntity
        """
        return self.__http.get_data_entity_by_id(id)

    def get_dataframe(self, data_entity: DataEntity) -> pd.DataFrame:
        """Getting DataFrame from DataEntity

        Read from DataEntity metadata attribute

        Note:
            If artifact's Uri is folder, reads first file from directory

        Args:
            data_entity (DataEntity): data entity

        Returns:
            pandas.DataFrame: pandas DataFrame
        """
        if self.__storage is None:
            raise Exception("Storage is not set")

        try:
            return self.__storage.get_dataframe(data_entity=data_entity)
        except Exception:
            raise

    def show_profile(self, data_frame: pd.DataFrame):
        """Get profile of DataEntity"""

        try:
            return self.__profiler.profile_to_notebook(data_frame)
        except Exception as e:
            logging.error(e)
            try:
                return self.__profiler.profile(data_frame)
            except Exception as e:
                raise ProfilerError("Could not get profile") from e

    def show_overview(self, data_entity_id: int):
        """Show details of DataEntity"""
        return self.__renderer.show_overview(data_entity_id)

    def show_structure(self, data_entity_id: int, structure_version_id: int):
        """Show structure of DataEntity"""
        return self.__renderer.show_structure(data_entity_id, structure_version_id)

    def show_lineage(self, data_entity_id: int):
        """Show lineage for DataEntity"""
        return self.__renderer.show_lineage(data_entity_id)

    def show_search_result(self, search_id: int):
        """Show search page"""
        return self.__renderer.show_search_result(search_id)
