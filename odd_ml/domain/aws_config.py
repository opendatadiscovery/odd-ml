from typing import Optional, Tuple
from pydantic import BaseSettings
from pydantic.env_settings import SettingsSourceCallable


class AwsConfig(BaseSettings):
    """AWS config

    Note:
        Secrets can be passed either from arguments or .env file.

    Attributes:
        aws_secret_access_key (str, optional): aws secret access key.
        aws_access_key_id (str, optional): aws access key id.
        aws_region (str, optional): aws region
        _env_file (str, optional): relative path to local .env file

    Examples:
        AwsConfig(_env_file='.env')

        AwsConfig(
            aws_secret_access_key='####',
            aws_access_key_id='####',
            aws_region='####'
        )

    """

    aws_secret_access_key: Optional[str]
    aws_access_key_id: Optional[str]
    aws_region: Optional[str]

    class Config:
        @classmethod
        def customize_sources(
            cls,
            init_settings: SettingsSourceCallable,
            env_settings: SettingsSourceCallable,
            file_secret_settings: SettingsSourceCallable,
        ) -> Tuple[SettingsSourceCallable, ...]:
            return env_settings, init_settings
