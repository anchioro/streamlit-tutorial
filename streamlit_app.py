import streamlit as st
import pandas as pd
import numpy as np

st.title("Viagens Uber NY City.")
DATA_URL = "https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz"

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    data.rename(lambda x: str(x).lower(), axis=1, inplace=True)
    data["date/time"] = pd.to_datetime(data["date/time"])
    return data

# Carregando os dados
data_load_state = st.text("Carregando dados...")
data = load_data(10000)
data_load_state.text("Carregamento dos dados foi realizado!")

# Exibindo os dados
if st.checkbox("Mostrar todos os dados."):
    st.write(data)

# Carregando a quantidade de viagens realizadas
st.subheader("Números de viagens por hora.")
hist_values = np.histogram(data["date/time"].dt.hour, bins=24, range=(0, 24))[0]

# Exibindo o gráfico
st.bar_chart(hist_values)

# Carregando e filtrando as quantidade de viagens realizadas durante determinada hora
hour_to_filter = st.slider("Hora", 0, 23, 12)
st.subheader(f"Mapa com todas as viagens realizadas durante {hour_to_filter}:00h.")
filtered_data = data[data["date/time"].dt.hour == hour_to_filter]

# Exibindo o mapa com a localização dos pedidos das viagens de cada hora
st.map(filtered_data)
