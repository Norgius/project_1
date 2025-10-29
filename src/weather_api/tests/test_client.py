import pytest
from pytest_httpx import HTTPXMock
from urllib.parse import urljoin

from weather_api import AsyncWeatherClient, BASE_URL, GetCurrentWeatherRequest, WeatherResponse


MOCK_RESPONSE = {
    "coord": {
        "lon": 39,
        "lat": 59
    },
    "weather": [{
        "id": 804,
        "main": "Clouds",
        "description": "пасмурно",
        "icon": "04n"
    }],
    "base": "stations",
    "main": {
        "temp": 4.03,
        "feels_like": 1.58,
        "temp_min": 4.03,
        "temp_max": 4.03,
        "pressure": 1006,
        "humidity": 96,
        "sea_level": 1006,
        "grnd_level": 985
    },
    "visibility": 952,
    "wind": {
        "speed": 2.7,
        "deg": 246,
        "gust": 5.11
    },
    "clouds": {
        "all": 100
    },
    "dt": 1761759118,
    "sys": {
        "country": "RU",
        "sunrise": 1761712465,
        "sunset": 1761745249
    },
    "timezone": 10800,
    "id": 569681,
    "name": "Чебсара",
    "cod": 200
}


@pytest.fixture
async def async_weather_client():
    async with AsyncWeatherClient.setup(api_key='api_key', timeout=3) as client:
        yield client


@pytest.mark.parametrize(
        'api_key',
        [
            '',
            ' ',
        ]
)
@pytest.mark.asyncio()
async def test_empty_api_key_error(api_key: str) -> None:
    with pytest.raises(ValueError, match=f'API_KEY for Weather Service is empty: {api_key}'):
        async with AsyncWeatherClient.setup(api_key=api_key):
            pass


@pytest.mark.asyncio()
async def test_valid_request(httpx_mock: HTTPXMock):
    mock_response = {
        "coord": {
            "lon": 39,
            "lat": 59,
        },
        "weather": [
            {
                "main": "Clouds",
                "description": "пасмурно"
            }
        ],
        "main": {
            "temp": 4.03,
            "temp_feels_like": 1.58,
            "pressure": 1006,
            "humidity": 96
        },
        "name": "Чебсара"
    }

    mock_url = urljoin(
        BASE_URL,
        '/data/2.5/weather?'
        'lon=59.0'
        '&lat=39.0'
        '&units=metric'
        '&lang=ru'
        '&appid=api_key',
    )

    httpx_mock.add_response(
        url=mock_url,
        json=MOCK_RESPONSE,
        method='GET',
    )

    async with AsyncWeatherClient.setup(api_key='api_key', timeout=3):
        request = GetCurrentWeatherRequest(
            lat=39,
            lon=59,
        )
        response = await request.asend()

        assert isinstance(response, WeatherResponse)
        assert response.model_dump(by_alias=False) == mock_response
