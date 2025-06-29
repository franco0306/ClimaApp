import streamlit as st
from utils.predictors import predecir_ciudad
from visuals.plotly_graphs import generar_figura_prediccion

from geopy.geocoders import Nominatim
import pandas as pd

st.set_page_config(page_title="Clima Futuro", layout="wide")
st.title("☀️🌧️ Predicción de Clima por Ciudad")



ciudad = st.text_input("Ingresa el nombre de una ciudad")

if st.button("Predecir clima"):
    with st.spinner("Obteniendo predicción..."):
        # Mostrar ubicación en el mapa
        geolocator = Nominatim(user_agent="miAppClima")
        location = geolocator.geocode(ciudad)
        if location:
            st.markdown("### 📍 Ubicación geográfica")
            st.map(pd.DataFrame({'lat': [location.latitude], 'lon': [location.longitude]}))

        future_df = predecir_ciudad(ciudad)
        if future_df is not None:
            fig = generar_figura_prediccion(future_df)
            st.plotly_chart(fig, use_container_width=True)
            st.dataframe(future_df)
        else:
            st.error("No se pudo generar la predicción.")
