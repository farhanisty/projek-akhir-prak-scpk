import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from DatasetProcessor import DatasetProcessor
from AHPComparison import AHPComparison

st.set_page_config(page_title="Visualisasi AHP COVID-19", layout="wide")
st.title("📊 Visualisasi Metode AHP pada Dataset COVID-19")

# Load dan proses dataset
@st.cache_data

def load_processed_data():
    processor = DatasetProcessor("dataset/data_covid.csv")
    return processor.pandasDatasetGroupedByLocation, processor.pandasDataset.columns.tolist()

cleanDataset, all_columns = load_processed_data()

st.subheader("🧹 Dataset yang Telah Diproses")
st.dataframe(cleanDataset, use_container_width=True)

# Tentukan jenis kriteria (True = Benefit, False = Cost)
st.subheader("⚙️ Tipe Kriteria")
st.markdown("Pilih jenis kriteria untuk setiap kolom:")
criteria_types = []
cols = st.columns(len(cleanDataset.columns))
for i, column in enumerate(cleanDataset.columns):
    is_benefit = cols[i].selectbox(f"{column}", ["Benefit", "Cost"]) == "Benefit"
    criteria_types.append(is_benefit)

# Input perbandingan antar kriteria menggunakan slider
st.subheader("🔢 Perbandingan Kriteria (Pairwise Matrix)")
comparison_matrix = np.ones((len(cleanDataset.columns), len(cleanDataset.columns)))
for i in range(len(cleanDataset.columns)):
    for j in range(i + 1, len(cleanDataset.columns)):
        weight = st.slider(f"Seberapa penting {cleanDataset.columns[i]} dibanding {cleanDataset.columns[j]}", 1, 9, 1)
        comparison_matrix[i][j] = weight
        comparison_matrix[j][i] = 1 / weight

# Buat objek AHP
criteriaComparison = AHPComparison(comparison_matrix, cleanDataset.columns, "Kriteria")

# Normalisasi data
@st.cache_data
def normalize_dataframe(df, criteria_types):
    df_norm = df.copy().astype(float)
    for i, column in enumerate(df.columns):
        if criteria_types[i]:
            df_norm[column] = df[column] / df[column].max()
        else:
            df_norm[column] = df[column].min() / df[column]
    return df_norm

normalizedDataset = normalize_dataframe(cleanDataset, criteria_types)

# Hitung skor dan ranking
scores = normalizedDataset @ criteriaComparison.weights
results_df = pd.DataFrame({
    "Lokasi": cleanDataset.index,
    "Skor AHP": scores
}).reset_index(drop=True)
results_df["Rangking"] = results_df["Skor AHP"].rank(ascending=False).astype(int)
results_df = results_df.sort_values("Rangking")

# Tampilkan hasil
st.subheader("🏆 Hasil Perangkingan Alternatif")
st.dataframe(results_df, use_container_width=True)

fig = px.bar(results_df, x="Lokasi", y="Skor AHP", color="Rangking",
             title="Skor AHP per Lokasi", text_auto='.2f',
             color_continuous_scale=px.colors.sequential.Tealgrn)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")
st.caption("💡 Proyek Akhir Sistem Pendukung Keputusan - AHP & COVID-19")
