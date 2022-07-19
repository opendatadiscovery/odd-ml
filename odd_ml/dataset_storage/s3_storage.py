import boto3
import pandas as pd
from s3path import S3Path

from odd_ml.dataset_storage.dataset_storage import DatasetStorage
from odd_ml.domain.aws_config import AwsConfig
from odd_ml.domain.data_entity import DataEntity
from odd_ml.helpers.get_s3_path import get_s3_path


class S3Storage(DatasetStorage):
    """Load s3 file from DataEntity metadata"""

    def __init__(self, config: AwsConfig) -> None:
        self.__config = config

        self.__setup_boto_session()

    def __setup_boto_session(self):
        """Create boto3 session"""
        boto3.setup_default_session(
            region_name=self.__config.aws_region,
            aws_access_key_id=self.__config.aws_access_key_id.get_secret_value(),
            aws_secret_access_key=self.__config.aws_secret_access_key.get_secret_value(),
        )

    def get_dataframe(self, data_entity: DataEntity) -> pd.DataFrame:
        return self.__read_path(get_s3_path(data_entity))

    def __read_path(self, uri: str):
        path = S3Path.from_uri(uri)

        if path.is_file():
            return self.__read_file(uri)
        elif path.is_dir():
            files = iter(path.iterdir())
            return self.__read_file(next(files).as_uri())
        else:
            raise ValueError("Unsupported path format")

    def __read_file(self, s3_uri: str):
        storage_options = {
            "key": self.__config.aws_access_key_id.get_secret_value(),
            "secret": self.__config.aws_secret_access_key.get_secret_value(),
        }

        args = {"filepath_or_buffer": s3_uri, "storage_options": storage_options}

        if s3_uri.endswith(".csv"):
            return pd.read_csv(**args)
        elif s3_uri.endswith(".parquet"):
            return pd.read_parquet(**args)
        else:
            raise ValueError(f"Unsupported file format {s3_uri}")
