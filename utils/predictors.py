import tensorflow as tf
import pandas as pd
from utils.data_fetcher import obtener_datos_nasa
from utils.preprocess import escalar_y_secuenciar
import numpy as np


def predecir_ciudad(ciudad):
    df = obtener_datos_nasa(ciudad)
    if df is None or len(df) < 20:
        return None

    features = ["temperatura", "temperatura_max", "temperatura_min", "viento", "precipitacion", "humedad"]

    # TEMPERATURA
    X_temp, y_temp, scaler = escalar_y_secuenciar(df, features, "temperatura", 10)
    modelo_temp = tf.keras.models.load_model("models/best_model.h5")
    last_seq = X_temp[-1]
    pred_temp = []
    for _ in range(14):
        pred = modelo_temp.predict(last_seq.reshape(1, 10, len(features)))[0][0]
        nuevo_dia = last_seq[-1].copy()
        nuevo_dia[0] = pred
        last_seq = np.vstack((last_seq[1:], nuevo_dia))
        pred_temp.append(pred)

    temp_inv = scaler.inverse_transform(np.repeat(np.array(pred_temp).reshape(-1, 1), len(features), axis=1))[:, 0]

    # LLUVIA
    X_rain, y_rain, _ = escalar_y_secuenciar(df, features, "lluvia", 10)
    modelo_rain = tf.keras.models.load_model("models/best_model_lluvia.keras")
    last_seq_rain = X_rain[-1]
    pred_rain = []
    for _ in range(14):
        pred = modelo_rain.predict(last_seq_rain.reshape(1, 10, len(features)))[0][0]
        nuevo_dia = last_seq_rain[-1].copy()
        last_seq_rain = np.vstack((last_seq_rain[1:], nuevo_dia))
        pred_rain.append(int(pred > 0.5))

    fechas = pd.date_range(start=df["dia"].iloc[-1] + pd.Timedelta(days=1), periods=14)
    return pd.DataFrame({"Fecha": fechas, "Temperatura": temp_inv, "Lluvia": pred_rain})
