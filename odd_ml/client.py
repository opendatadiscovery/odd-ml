import json
from typing import Tuple, TypeVar, Type, List, Optional
from pydantic.env_settings import SettingsSourceCallable

import boto3
import pandas
import requests
from pydantic import BaseModel, BaseSettings, SecretStr
from s3path import S3Path

from odd_ml.domain.data_entity import DataEntity, MetadataFiled
from odd_ml.domain.data_source import GetDataSourcesResult
from odd_ml.domain.search import (
    SearchFormData,
    SearchFormDataFilters,
    SearchFilterState,
    SearchResult,
)

T = TypeVar("T", bound=BaseModel)


class AwsConfig(BaseSettings):
    aws_secret_access_key: Optional[str]
    aws_access_key_id: Optional[str]
    aws_region: str

    class Config:
        @classmethod
        def customise_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> Tuple[SettingsSourceCallable, ...]:
            return env_settings, init_settings


class Client:
    def __init__(self, platform_url, aws_config: AwsConfig):
        self.platform_url = platform_url
        self.aws_settings = aws_config

        self.__setup_boto_session()

    def __setup_boto_session(self):
        session = boto3.Session(region_name=self.aws_settings.aws_region)
        access_key = (
            self.aws_settings.aws_access_key_id or session.get_credentials().access_key
        )

        secret_key = (
            self.aws_settings.aws_secret_access_key
            or session.get_credentials().secret_key
        )

        boto3.setup_default_session(
            region_name=self.aws_settings.aws_region,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
        )

    def __get_search_id(self, query: str, datasource_id: int = None) -> str:
        filters = SearchFormDataFilters()

        if datasource_id is not None:
            filters.datasources = [
                SearchFilterState(entity_id=datasource_id, selected=True)
            ]

        data = SearchFormData(
            query=query,
            filters=filters,
        )

        res = requests.post(
            url=f"{self.platform_url}/api/search",
            data=data.json(),
            headers={"Content-Type": "application/json"},
        )
        res.raise_for_status()

        return json.loads(res.text).get("search_id")

    def search(self, query: str, datasource_id: int = None) -> SearchResult:
        search_id = self.__get_search_id(query, datasource_id)
        url = f"{self.platform_url}/api/search/{search_id}/results?page=1&size=30"

        return self.__get(url, SearchResult)

    def get_data_sources(self):
        return self.__get(
            f"{self.platform_url}/api/datasources?page=1&size=100", GetDataSourcesResult
        )

    def get_data_entity_by_id(self, id: int):
        return self.__get(f"{self.platform_url}/api/dataentities/{id}", DataEntity)

    def __read_file(self, s3_uri: str):
        storage_options = {
            "key": self.aws_settings.aws_access_key_id,
            "secret": self.aws_settings.aws_secret_access_key,
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

    def __read_path(self, uri: str):
        path = S3Path.from_uri(uri)

        if path.is_file():
            return self.__read_file(uri)
        elif path.is_dir():
            files = (file_path for file_path in path.iterdir())
            return self.__read_file(next(files).as_uri())
        else:
            raise ValueError("Unsupported path format")

    def get_dataframe(self, de: DataEntity):
        s3_uri = self.__find_s3_uri(de.metadata_field_values)

        return self.__read_path(s3_uri)

    @staticmethod
    def __find_s3_uri(xs: List[MetadataFiled]) -> Optional[str]:
        filtered = [x.value for x in xs if x.field.name == "Uri"]

        if (length := len(filtered)) == 0:
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
