import logging
from contextlib import asynccontextmanager

from pydantic import BaseModel
from fastapi import FastAPI, HTTPException
from starlette import status

from settings import env
from weather_api import (
    AsyncWeatherClient,
    GetCurrentWeatherRequest,
    WeatherResponse,
    WeatherServiceError
)

logger = logging.getLogger('__name__')


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with AsyncWeatherClient().setup(env.WEATHER_SERVICE.API_KEY):
        yield


app = FastAPI(lifespan=lifespan)


class WeatherError(BaseModel):
    detail: str | dict[str, str]


@app.get(
        '/',
        response_model=WeatherResponse,
        responses={
            status.HTTP_200_OK: {'model': WeatherResponse},
            status.HTTP_400_BAD_REQUEST: {'model': WeatherError},
        },
        summary='Получить погоду по координатам, координаты временно замоканы',
)
async def get_weather() -> WeatherResponse:
    try:
        # Временно для всех параметров класса GetCurrentWeatherRequest есть данные по-умолчанию
        request = GetCurrentWeatherRequest()
        return await request.asend()
    except WeatherServiceError as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Weather Service Error',
        )
