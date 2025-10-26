from contextlib import asynccontextmanager

import httpx


class WeatherAsyncClientError(Exception):
    pass


ERROR_MESSAGES = {
    httpx.TimeoutException: "Timeout connecting to WeatherService",
    httpx.RequestError: "Network issue contacting WeatherService",
}


class WeatherServiceError(Exception):

    @classmethod
    @asynccontextmanager
    async def async_reraise_from(
        cls,
        *exc: type[Exception],
        msg: str = 'Weather Service Error',
    ):
        if not exc:
            exc = (Exception,)

        try:
            yield
        except exc as e:
            raise cls(f'{msg}: {e!r}') from e
        except Exception as e:
            raise cls(f'{msg}. Attention! Unexpected exception: {e!r}') from e
