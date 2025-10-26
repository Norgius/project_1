from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class WeatherServiceSettings(BaseModel):
    API_KEY: SecretStr


class ENV(BaseSettings):
    WEATHER_SERVICE: WeatherServiceSettings
    """Настройки API для сервиса погоды"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        validate_default=True,
        extra="forbid",
        use_attribute_docstrings=True,
    )


env = ENV()
