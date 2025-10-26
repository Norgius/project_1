from pydantic import ConfigDict, BaseModel, Field


response_config = ConfigDict(
    validate_default=True,
    extra="ignore",
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
    main: WeatherMainData

    model_config = response_config
