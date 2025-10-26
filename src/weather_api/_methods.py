
from typing import Literal

from httpx import HTTPStatusError, RequestError, TimeoutException
from pydantic import BaseModel, ConfigDict

from ._api_client import AsyncWeatherClient
from ._api_types import WeatherResponse
from ._exceptions import WeatherServiceError


async def aget(request: BaseModel) -> bytes:
    client = AsyncWeatherClient.get_initialized_instance()
    async with WeatherServiceError.async_reraise_from(TimeoutException, HTTPStatusError, RequestError):
        response = await client.get(request.endpoint, params=request.model_dump(exclude='endpoint'))
        response.raise_for_status()

    return response


class GetCurrentWeatherRequest(BaseModel):
    endpoint: str = '/data/2.5/weather'
    lat1: float = 59.222266
    lon: float = 39.915175
    units: Literal['metric', 'default'] = 'metric'
    lang: Literal['ru', 'en'] = 'ru'

    model_config = ConfigDict(
        extra='forbid',
    )

    async def asend(self) -> WeatherResponse:
        response = await aget(self)
        return WeatherResponse.model_validate_json(response.content)
