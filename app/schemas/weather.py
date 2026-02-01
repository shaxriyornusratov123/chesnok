from pydantic import BaseModel


class WeatherCoord(BaseModel):
    lon: float
    lat: float


class WeatherInline(BaseModel):
    id: int
    main: str
    description: str
    icon: str


class WeatherMain(BaseModel):
    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int


class WeatherResponse(BaseModel):
    coord: WeatherCoord
    weather: list[WeatherInline]
    # base: str
    # main: WeatherMain
    # visibility: int
    # wind: dict[str, float] | None = None
    # rain: dict[str, float] | None = None
    # clouds: dict[str, int] | None = None
    # dt: int
    # sys: dict[str, int | str] | None = None
    # timezone: int
    # id: int
    # name: str
    # cod: int
