import httpx  # requests capability, but can work with async
from prefect import flow, task


@task
def fetch_weather(lat: float, lon: float):
    base_url = "https://api.open-meteo.com/v1/forecast/"
    weather = httpx.get(
        base_url,
        params=dict(latitude=lat, longitude=lon, hourly="temperature_2m"),
    )
    most_recent_temp = float(weather.json()["hourly"]["temperature_2m"][0])
    return most_recent_temp


@task
def fetch_precipitation(lat: float, lon: float):
    base_url = "https://api.open-meteo.com/v1/forecast/"

    weather_feature = "precipitation_probability"
    weather = httpx.get(
        base_url,
        params=dict(latitude=lat, longitude=lon, hourly=weather_feature),
    )
    most_recent_prec_prob = float(weather.json()["hourly"][weather_feature][0])
    return most_recent_prec_prob


@task
def save_weather(temp: float):
    with open("weather.csv", "w+") as w:
        w.write(str(temp))
    return "Successfully wrote temp"


@task
def save_precipitation(pp: float):
    with open("precipitation_probability.csv", "w+") as w:
        w.write(str(pp))
    return "Successfully wrote precipitation probability"


@task
def fetch_hourly_weather_feature(lat: float, lon: float, weather_feature: str):
    base_url = "https://api.open-meteo.com/v1/forecast/"

    weather = httpx.get(
        base_url,
        params=dict(latitude=lat, longitude=lon, hourly=weather_feature),
    )
    most_recent_prec_prob = float(weather.json()["hourly"][weather_feature][0])
    return most_recent_prec_prob


@task
def calc_sunscreen_level(uv_index: float):
    sunscreen_level = 10 * (1 + uv_index) ** 2
    return sunscreen_level


@task
def save_sunscreen_level(sunscreen_level: float):
    with open("sunscreen_level.csv", "w+") as w:
        w.write(str(sunscreen_level))
    return "Successfully wrote precipitation probability"


@flow(log_prints=True)
def pipeline(lat: float, lon: float):
    uv_index = fetch_hourly_weather_feature(lat, lon, weather_feature="uv_index")
    sunscreen_level = calc_sunscreen_level(uv_index)
    result = save_sunscreen_level(sunscreen_level)
    return result


if __name__ == "__main__":
    pipeline(38.9, -77.0)
