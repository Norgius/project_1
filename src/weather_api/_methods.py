
from typing import Annotated, Literal

from httpx import HTTPStatusError, RequestError, TimeoutException
from pydantic import AfterValidator, BaseModel, ConfigDict

from ._api_client import AsyncWeatherClient
from ._api_types import WeatherResponse
from ._exceptions import WeatherServiceError


def lon_coord_validator(coord: float):
    if not -180 <= coord <= 180:
        raise ValueError('Latitude must be between -90 and 90.')
    return coord


def lan_coord_validator(coord: float):
    if not -180 <= coord <= 180:
        raise ValueError('Longitude must be between -180 and 180.')
    return coord


async def aget(request: BaseModel) -> bytes:
    client = AsyncWeatherClient.get_initialized_instance()
    async with WeatherServiceError.async_reraise_from(TimeoutException, HTTPStatusError, RequestError):
        response = await client.get(request._endpoint, params=request.model_dump())
        response.raise_for_status()

    return response


class GetCurrentWeatherRequest(BaseModel):
    _endpoint: str = '/data/2.5/weather'
    lat: Annotated[float, AfterValidator(lan_coord_validator)]
    lon: Annotated[float, AfterValidator(lon_coord_validator)]
    units: Literal['metric', 'default'] = 'metric'
    lang: Literal['ru', 'en'] = 'ru'

    model_config = ConfigDict(
        extra='forbid',
    )

    async def asend(self) -> WeatherResponse:
        response = await aget(self)
        return WeatherResponse.model_validate_json(response.content)
