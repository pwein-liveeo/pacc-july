import httpx  # requests capability, but can work with async
from prefect import flow, task


@task
def fetch_weather(lat: float, lon: float):
    base_url = "https://api.open-meteo.com/v1/forecast/"
    weather = httpx.get(
        base_url,
        params=dict(latitude=lat, longitude=lon),
    )
    return weather


@task
def read_temperature_from_weather(weather):
    most_recent_temp = float(weather.json()["hourly"]["temperature_2m"][0])
    return most_recent_temp


@task
def read_precipitation_probability_from_weather(weather):
    precipitation_prob = float(weather.json()["hourly"]["Precipitation Probability"][0])
    return precipitation_prob


@task
def save_weather(temp: float):
    with open("weather.csv", "w+") as w:
        w.write(str(temp))
    return "Successfully wrote temp"


@flow
def pipeline(lat: float, lon: float):
    weather = fetch_weather(lat, lon)

    print(weather.json())
    # temp = read_temperature_from_weather(weather)
    # precipitation_prob = read_precipitation_probability_from_weather(weather)

    # result = save_weather(temp)
    # return result


if __name__ == "__main__":
    pipeline(38.9, -77.0)
