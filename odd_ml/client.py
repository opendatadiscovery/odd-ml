import json
from typing import TypeVar, Type, List, Optional

import boto3
import pandas
import requests
from pydantic import BaseModel


from s3path import S3Path
from odd_ml.domain.aws_config import AwsConfig
from odd_ml.domain.data_entity import DataEntity, MetadataFiled
from odd_ml.domain.data_source import GetDataSourcesResult
from odd_ml.domain.search import (
    SearchFormData,
    SearchFormDataFilters,
    SearchFilterState,
    SearchResult,
)
from odd_ml.renderer import IFrameRenderer

T = TypeVar("T", bound=BaseModel)

# TODO: Create separated HttpClient, move all api logic to him
# TODO: Create separated s3 reader class, move chained logic to him
# TODO: Create domain exceptions
class Client:
    """Client for retrieving data from odd-platform"""

    def __init__(self, platform_url, aws_config: AwsConfig):
        """Creating client

        Args:
            platform_url (str): url to odd-platform
            aws_config (AwsConfig): aws config
        """
        self.__url = platform_url
        self.__aws_config = aws_config
        self.__setup_boto_session()
        self.__renderer = IFrameRenderer(platform_url)

    # TODO: add more id for filter (i.e: namespace_id: id, ...)
    def search(self, query: str, datasource_id: int = None) -> SearchResult:
        """Search any data entity

        Args:
            query (str): searching text
            datasource_id (int, optional): datasource id for narrowing search. Defaults to None.

        Returns:
            SearchResult
        """
        search_id = self.__get_search_id(query, datasource_id)
        url = f"{self.__url}/api/search/{search_id}/results?page=1&size=30"

        return self.__get(url, SearchResult)

    def get_data_sources(self) -> GetDataSourcesResult:
        """List of all DataSources

        Returns:
            GetDataSourcesResult
        """
        return self.__get(
            f"{self.__url}/api/datasources?page=1&size=100", GetDataSourcesResult
        )

    def get_data_entity_by_id(self, id: int) -> DataEntity:
        """Getting data entity id

        Args:
            id (int): id of data entity

        Returns:
            DataEntity
        """
        return self.__get(f"{self.__url}/api/dataentities/{id}", DataEntity)

    def get_dataframe(self, de: DataEntity) -> pandas.DataFrame:
        """Getting DataFrame from DataEntity

        Read from DataEntity metadata attribute

        Note:
            If artifact's Uri is folder, reads first file from directory

        Args:
            de (DataEntity): data entity

        Returns:
            pandas.DataFrame: _description_
        """
        s3_uri = self.__find_s3_uri(de.metadata_field_values)

        return self.__read_path(s3_uri)

    def show_overview(self, data_entity_id: int):
        """Show details of DataEntity"""
        return self.__renderer(data_entity_id)

    def show_structure(self, data_entity_id: int, structure_version_id: int):
        """Show structure of DataEntity"""
        return self.__renderer.show_structure(data_entity_id, structure_version_id)

    def show_lineage(self, data_entity_id: int):
        """Show lineage for DataEntity"""
        return self.__renderer.show_lineage(data_entity_id)

    def show_search_result(self, search_id: int):
        """Show search page"""
        return self.__renderer.show_search_result(search_id)

    def __read_file(self, s3_uri: str):
        storage_options = {
            "key": self.__aws_config.aws_access_key_id,
            "secret": self.__aws_config.aws_secret_access_key,
        }
        if s3_uri.endswith(".csv"):
            return pandas.read_csv(
                s3_uri,
                storage_options=storage_options,
            )
        elif s3_uri.endswith(".parquet"):
            return pandas.read_parquet(
                s3_uri,
                storage_options=storage_options,
            )
        else:
            raise ValueError(f"Unsupported file format {s3_uri}")

    def __setup_boto_session(self):
        """Create boto3 session"""
        session = boto3.Session(region_name=self.__aws_config.aws_region)
        access_key = (
            self.__aws_config.aws_access_key_id or session.get_credentials().access_key
        )

        secret_key = (
            self.__aws_config.aws_secret_access_key
            or session.get_credentials().secret_key
        )

        boto3.setup_default_session(
            region_name=self.__aws_config.aws_region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

    def __get_search_id(self, query: str, datasource_id: int = None) -> str:
        """Each search request needs hashed search id from platform

        Returns:
            str: if successfull, else raises HTTPError

        Raises:
            HTTPError: in case of server returned error
        """
        filters = SearchFormDataFilters()

        # TODO: Add more filter
        if datasource_id is not None:
            filters.datasources = [
                SearchFilterState(entity_id=datasource_id, selected=True)
            ]

        data = SearchFormData(
            query=query,
            filters=filters,
        )

        res = requests.post(
            url=f"{self.__url}/api/search",
            data=data.json(),
            headers={"Content-Type": "application/json"},
        )
        res.raise_for_status()

        return json.loads(res.text).get("search_id")

    def __read_path(self, uri: str):
        path = S3Path.from_uri(uri)

        if path.is_file():
            return self.__read_file(uri)
        elif path.is_dir():
            files = iter(path.iterdir())
            return self.__read_file(next(files).as_uri())
        else:
            raise ValueError("Unsupported path format")

    @staticmethod
    def __find_s3_uri(xs: List[MetadataFiled]) -> Optional[str]:
        filtered = [x.value for x in xs if x.field.name == "Uri"]

        length = len(filtered)
        if length == 0:
            raise ValueError("Could not find Uri in metadata")
        elif length > 1:
            raise ValueError("Found more than one metadata with field Uri")
        else:
            return filtered[0]

    @staticmethod
    def __get(url, cls: Type[T]) -> T:
        res = requests.get(url)
        res.raise_for_status()
        return cls.parse_raw(res.text)
