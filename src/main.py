import logging
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel
from starlette import status

from settings import env
from weather_api import AsyncWeatherClient, GetCurrentWeatherRequest, WeatherResponse, WeatherServiceError

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
            status.HTTP_422_UNPROCESSABLE_CONTENT: {'model': WeatherError},
        },
        summary='Погода по координатам',
)
async def get_weather(request: GetCurrentWeatherRequest = Depends()) -> WeatherResponse:
    try:
        return await request.asend()
    except WeatherServiceError as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Weather Service Error',
        )
