# dashboard_transporte.py
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Dashboard de Mobilidade", layout="wide")
st.title("Dashboard de Mobilidade - Transporte Público")

# --- Dados fictícios ---
np.random.seed(42)
estacoes = ["Trindade", "Campanhã", "Bolhão", "Aliados", "Casa da Música"]
horas = list(range(6, 23))  # das 6h às 22h

data = []
for est in estacoes:
    for hora in horas:
        passageiros = np.random.randint(50, 500)  # número fictício de passageiros
        data.append({"estacao": est, "hora": hora, "passageiros": passageiros})

df = pd.DataFrame(data)

# --- Filtros ---
st.sidebar.header("Filtros")
estacao_selecionada = st.sidebar.selectbox("Escolhe a estação", estacoes)
df_filtrado = df[df['estacao'] == estacao_selecionada]

# --- Gráfico de linha ---
st.subheader(f"Passageiros por hora na estação {estacao_selecionada}")
fig_linha = px.line(df_filtrado, x='hora', y='passageiros',
                    labels={"hora": "Hora do dia", "passageiros": "Número de passageiros"},
                    markers=True)
st.plotly_chart(fig_linha, use_container_width=True)

# --- Heatmap de todas as estações ---
st.subheader("Comparação de todas as estações")
fig_heatmap = px.density_heatmap(df, x='hora', y='estacao', z='passageiros',
                                 color_continuous_scale='Viridis',
                                 labels={"hora": "Hora do dia", "estacao": "Estação", "passageiros": "Passageiros"})
st.plotly_chart(fig_heatmap, use_container_width=True)

# --- Mapa interativo (simulado) ---
st.subheader("Mapa interativo das estações (simulado)")
# Coordenadas fictícias
coords = {
    "Trindade": [41.147, -8.611],
    "Campanhã": [41.157, -8.600],
    "Bolhão": [41.145, -8.610],
    "Aliados": [41.149, -8.610],
    "Casa da Música": [41.160, -8.630]
}
map_data = pd.DataFrame({
    "estacao": estacoes,
    "lat": [coords[e][0] for e in estacoes],
    "lon": [coords[e][1] for e in estacoes],
    "passageiros": [df[df['estacao']==e]['passageiros'].sum() for e in estacoes]
})

fig_map = px.scatter_mapbox(map_data, lat="lat", lon="lon", size="passageiros",
                            hover_name="estacao", color="passageiros", zoom=13,
                            mapbox_style="open-street-map")
st.plotly_chart(fig_map, use_container_width=True)
