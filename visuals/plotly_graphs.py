import plotly.graph_objects as go

def generar_figura_prediccion(df):
    texto_hover = [
        f"Fecha: {f.strftime('%Y-%m-%d')}<br>Temp: {t:.2f}°C<br>Lluvia: {'Sí' if l == 1 else 'No'}"
        for f, t, l in zip(df["Fecha"], df["Temperatura"], df["Lluvia"])
    ]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["Fecha"], y=df["Temperatura"], mode="lines+markers",
        text=texto_hover, hoverinfo="text", name="Temperatura Futura"
    ))

    fig.update_layout(
        title="Predicción de Temperatura y Lluvia",
        xaxis_title="Fecha",
        yaxis_title="°C",
        template="plotly_dark"
    )
    return fig
