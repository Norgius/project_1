from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any, Self

import httpx
from pydantic import SecretStr

from ._exceptions import WeatherAsyncClientError

BASE_URL = 'https://api.openweathermap.org'


class AsyncWeatherClient(httpx.AsyncClient):
    _initialized_instance = None

    def __init__(self, api_key: str = '', *args: Any, **kwargs: Any):
        self.api_key = api_key
        kwargs['base_url'] = kwargs.get('base_url', BASE_URL)
        super().__init__(*args, **kwargs)

    @classmethod
    @asynccontextmanager
    async def setup(cls, api_key: SecretStr | str = '', *args: Any, **kwargs: Any) -> AsyncGenerator[None]:
        if isinstance(api_key, SecretStr):
            api_key = api_key.get_secret_value()
        else:
            raise ValueError(f'API_KEY for Weather Service is empty: {api_key}')
        cls._initialized_instance = cls(api_key, *args, **kwargs)
        async with cls._initialized_instance:
            yield

    @classmethod
    def get_initialized_instance(cls) -> Self:
        if initialized_instance := cls._initialized_instance:
            return initialized_instance
        raise WeatherAsyncClientError(
            'Клиент AsyncWeatherClient не был проинициализирован. ',
            'Воспользуйтесь методом setup() для инициализации клиента',
        )

    async def request(self, *args: Any, **kwargs: Any) -> httpx.Response:
        params = kwargs.pop('params', {})
        params['appid'] = self.api_key
        return await super().request(*args, params=params, **kwargs)
