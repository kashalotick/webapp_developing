from typing import Annotated

from fastapi import Depends
from pydantic_settings import BaseSettings, SettingsConfigDict, JsonConfigSettingsSource


class ApiConfig(BaseSettings):
    model_config = SettingsConfigDict(json_file="api_config.json", json_file_encoding="utf-8")

    readonly: bool
    page_size: int
    @classmethod
    def settings_customise_sources(
            cls,
            settings_cls,
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings
    ):
        return (init_settings, JsonConfigSettingsSource(settings_cls), env_settings)


api_config = ApiConfig()

ApiConfigDep = Annotated[ApiConfig, Depends(lambda :api_config)]
