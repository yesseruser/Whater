import urllib.parse
import urllib.request
import json
import urllib.error
from platformdirs import user_data_dir
import os.path

key_file = os.path.join(user_data_dir("whather", "yesseruser", ensure_exists=True), "key.txt")
print(key_file)


def set_key(key: str):
    with open(key_file, "a") as file:
        file.write(key)


def get_key() -> str:
    if not os.path.isfile(key_file):
        return ""

    with open(key_file, "r") as file:
        return file.readline()


def delete_key():
    if not os.path.isfile(key_file):
        return

    os.remove(key_file)


Key = get_key()
Url = "https://api.openweathermap.org/data/2.5/weather"
IconUrl = "https://openweathermap.org/img/wn/"


def get_api_params(city: str) -> dict:
    return {
        "appid": Key,
        "units": "metric",
        "lang": "cz",
        "q": city
    }


def get_api_response(params: dict) -> dict:
    print("Získávání informací o počasí v " + str(params["q"]).capitalize())
    params = urllib.parse.urlencode(params)
    try:
        response = urllib.request.urlopen(Url + "?" + params)
        return json.loads(response.read().decode())
    except urllib.error.HTTPError as error:
        if error.code == 401:
            print("Zkontrolujte klíč.")
        else:
            print("Chyba HTTP: Zkotrolujte zadaný název města")
        exit()
    except urllib.error.URLError:
        print("Chyba URL: Zkontrolujte připojení k internetu")
        exit()


def get_current_weather(city: str):
    params = get_api_params(city)
    response = get_api_response(params)
    return get_weather_object(response)


def get_weather_object(data: dict) -> dict:
    return {
        "desc": str(data["weather"][0]["description"]),
        "temp": str(data["main"]["temp"]) + "°C",
        "feels_like": str(data["main"]["feels_like"]) + "°C",
        "press": str(data["main"]["pressure"]) + "hPa",
        "speed": str(data["wind"]["speed"]) + "m/s",
        "deg": str(data["wind"]["deg"]) + "° vpravo od severu",
        "icon": IconUrl + (data["weather"][0]["icon"]) + "@2x.png"
    }


def print_weather_info(w: dict):
    print(str(w["desc"]).capitalize())
    print("Teplota: " + str(w["temp"]))
    print("Pocitová teplota: " + str(w["feels_like"]))
    print("Atmosférický tlak: " + str(w["press"]))
    print("Rychlost větru: " + str(w["speed"]))
    print("Směr větru: " + str(w["deg"]))
    print("Ikona(Webová stránka): " + str(w["icon"]))