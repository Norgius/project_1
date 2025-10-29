from pydantic import BaseModel, ConfigDict, Field

response_config = ConfigDict(
    validate_default=True,
    extra="ignore",
    use_attribute_docstrings=True,
)


class Coordinates(BaseModel):
    lat: float
    lon: float

    model_config = response_config


class WeatherDescription(BaseModel):
    main: str = 'Clouds'
    description: str

    model_config = response_config


class WeatherMainData(BaseModel):
    temp: float
    temp_feels_like: float = Field(alias='feels_like')
    pressure: int
    humidity: int

    model_config = response_config


class WeatherResponse(BaseModel):
    coord: Coordinates
    weather: list[WeatherDescription]
    """Текстовое описание погоды."""
    main: WeatherMainData
    """Числовые метеорологические значения."""
    name: str
    """Название города/населённого пункта."""

    model_config = response_config
