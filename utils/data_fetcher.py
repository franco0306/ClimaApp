import requests
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
import pandas as pd

def obtener_datos_nasa(ciudad):
    today = datetime.now()
    start_date = (today - timedelta(days=2 * 365)).strftime("%Y-%m-%d")
    end_date = (today - timedelta(days=5)).strftime("%Y-%m-%d")

    geolocator = Nominatim(user_agent="miAPI")
    location = geolocator.geocode(ciudad)

    if not location:
        return None

    lat, lon = location.latitude, location.longitude

    url = "https://power.larc.nasa.gov/api/temporal/daily/point"
    params = {
        "start": start_date.replace("-", ""),
        "end": end_date.replace("-", ""),
        "latitude": lat,
        "longitude": lon,
        "community": "re",
        "parameters": "T2M,T2M_MAX,T2M_MIN,PRECTOTCORR,RH2M,WS2M",
        "format": "json",
        "user": "streamlit",
        "header": "true",
        "time-standard": "utc"
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        return None

    nasa_data = response.json()['properties']['parameter']
    registros = []
    for fecha in nasa_data['T2M']:
        dia = datetime.strptime(fecha, "%Y%m%d").date()
        registros.append({
            "dia": dia,
            "temperatura": nasa_data['T2M'][fecha],
            "temperatura_max": nasa_data['T2M_MAX'].get(fecha),
            "temperatura_min": nasa_data['T2M_MIN'].get(fecha),
            "precipitacion": nasa_data['PRECTOTCORR'].get(fecha),
            "humedad": nasa_data['RH2M'].get(fecha),
            "viento": nasa_data['WS2M'].get(fecha),
            "ciudad": ciudad,
        })

    df = pd.DataFrame(registros)
    df["lluvia"] = df.apply(lambda row: 1 if (row["precipitacion"] > 0.2 and row["humedad"] > 80) else 0, axis=1)
    df = df.dropna()
    return df
