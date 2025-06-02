import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from DatasetProcessor import DatasetProcessor
from AHPComparison import AHPComparison


st.set_page_config(page_title="Visualisasi AHP COVID-19", layout="wide")

def highlight_benefit_cost(val):
    if val == "Benefit":
        return "background-color: #00ff00; color: black; font-weight: bold;"  # Hijau muda
    elif val == "Cost":
        return "background-color: #ff0000; color: black; font-weight: bold;"  # Merah muda
    return ""

def get_data_info(df):
    return f"Total baris: {df.shape[0]} | Total kolom: {df.shape[1]}"

@st.cache_data
def normalize_dataframe(df, criteria_types):
    df_norm = df.copy().astype(float)

    for i, column in enumerate(df.columns):
        if criteria_types[i]:  # Benefit
            df_norm[column] = df[column] / df[column].max()
        else:  # Cost
            df_norm[column] = df[column].min() / df[column]
    
    return df_norm

with st.sidebar:
    st.header("Projek Akhir SCPK")
    halaman = st.sidebar.radio("", ["Pendahuluan", "Proses Data", "AHP"])

@st.cache_data
def load_processed_data():
    processor = DatasetProcessor("dataset/data_covid.csv")
    return processor.pandasDatasetGroupedByLocation, processor.pandasDataset.columns.tolist()

cleanDataset, all_columns = load_processed_data()
datasetProcessor = DatasetProcessor("dataset/data_covid.csv")

if halaman == "Pendahuluan":
    st.title("Pemilihan provinsi prioritas untuk distribusi vaksin dengan pendekatan AHP")
    st.image("img/ilustrasi-vaksin.jpeg", caption="Distribusi Vaksin", use_container_width=True)
    st.subheader("Anggota Kelompok")
    st.write("""
        - Farhannivta Ramadhana(123230139)
        - Muhammad Aditya(123230145)
    """)

    st.subheader("Deskripsi")
    st.write("""
Proyek ini bertujuan untuk mengeksplorasi penerapan metode Analytic Hierarchy Process (AHP) dalam membantu proses pengambilan keputusan. Sebagai studi kasus, proyek ini mensimulasikan proses penentuan provinsi-provinsi yang diprioritaskan untuk distribusi vaksin di Indonesia.

Melalui tahapan penyusunan hierarki, perbandingan antar alternatif, dan perhitungan bobot, metode AHP digunakan untuk menghasilkan urutan prioritas berdasarkan sejumlah faktor yang telah ditentukan. Proyek ini difokuskan pada pemahaman konsep dan mekanisme kerja AHP dalam konteks pengambilan keputusan multi-kriteria.
             """)

    st.subheader("Dataset")
    st.write("""
    Deskripsi Dataset:
    Dataset ini berisi data harian terkait pandemi COVID-19 di Indonesia, yang dikumpulkan dari sumber resmi. Tujuan dari pembuatan dataset ini adalah untuk membantu dalam pengambilan keputusan dengan mempertimbangkan berbagai faktor yang relevan.

    - Sumber Data: [Kaggle - COVID19 Indonesia](https://www.kaggle.com/datasets/hendratno/covid19-indonesia)

    - Format: CSV

    - Ukuran File: 7.5 MB

    - Jumlah File: 1

    Dataset ini mencakup informasi harian tentang kasus COVID-19 di Indonesia, termasuk jumlah kasus terkonfirmasi, sembuh, dan meninggal, yang dapat digunakan untuk analisis tren dan pengambilan keputusan.
    """)
elif halaman == "Proses Data": 
    steps = [
    ("Data Mentah", datasetProcessor.pandasDataset),
    ("Data 2 bulan terbaru", datasetProcessor.pandasDatasetTowLatestMonth),
    ("Data dengan kolom yang diperlukan", datasetProcessor.pandasDatasetFilteredByUsedColumns),
    ("Data dengan kolom 'Location' hanya berupa provinsi", datasetProcessor.pandasDatasetNotIncludeIndonesiaLocation),
    ("Data group berdasarkan provinsi (Data Final)", datasetProcessor.pandasDatasetGroupedByLocation)
    ]


    if "step_idx" not in st.session_state:
        st.session_state.step_idx = 0

    def next_step():
        if st.session_state.step_idx < len(steps) - 1:
            st.session_state.step_idx += 1

    def prev_step():
        if st.session_state.step_idx > 0:
            st.session_state.step_idx -= 1

    st.title("Proses Pembersihan Data")
    st.subheader(f"Langkah {st.session_state.step_idx + 1}: {steps[st.session_state.step_idx][0]}")


    st.dataframe(steps[st.session_state.step_idx][1].head(50), use_container_width=True)

    judul, data = steps[st.session_state.step_idx]
    st.markdown(get_data_info(data))

    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        if st.button("⬅️ Prev"):
            prev_step()

    with col3:
        if st.button("Next ➡️"):
            next_step()
else:
    st.header("AHP")

    st.subheader("📊 Data siap proses")
    st.dataframe(datasetProcessor.pandasDatasetGroupedByLocation, use_container_width=True)

    kriteria_data = {
        "Kriteria": [
            "Population Density",
            "Total Recovered",
            "Total Deaths",
            "Total Cases",
            "New Cases"
        ],
        "Jenis": [
            "Benefit",
            "Cost",
            "Benefit",
            "Benefit",
            "Benefit"
        ]
    }

    st.subheader("📋 Jenis Kriteria Setiap Kolom")
    df_kriteria = pd.DataFrame(kriteria_data)
    styled_df = df_kriteria.style.applymap(highlight_benefit_cost, subset=["Jenis"])

    st.table(styled_df.hide(axis="index"))

    normalizedDataframe = normalize_dataframe(datasetProcessor.pandasDatasetGroupedByLocation, [True, False, True, True, True])
    st.subheader("⚙️ Normalisasi")
    st.dataframe(normalizedDataframe, use_container_width=True)

    st.subheader("🔢 Input Pairwise Kriteria")

    populationDensity = st.slider("Population Density", min_value=0.1, max_value=10.0, value=2.0)
    totalRecovered = st.slider("Total Recovered", min_value=0.1, max_value=10.0, value=2.0)
    totalDeaths = st.slider("Total Deaths", min_value=0.1, max_value=10.0, value=2.0)
    totalCases = st.slider("Total Cases", min_value=0.1, max_value=10.0, value=2.0)
    newCases = st.slider("New Cases", min_value=0.1, max_value=10.0, value=2.0)

    pairwise_inputs = [
        [populationDensity/populationDensity, populationDensity/totalRecovered, populationDensity/totalDeaths, populationDensity/totalCases, populationDensity/newCases],
        [totalRecovered/populationDensity, totalRecovered/totalRecovered, totalRecovered/totalDeaths, totalRecovered/totalCases, totalRecovered/newCases],
        [totalDeaths/populationDensity, totalDeaths/totalRecovered, totalDeaths/totalDeaths, totalDeaths/totalCases, totalDeaths/newCases],
        [totalCases/populationDensity, totalCases/totalRecovered, totalCases/totalDeaths, totalCases/totalCases, totalCases/newCases],
        [newCases/populationDensity, newCases/totalRecovered, newCases/totalDeaths, newCases/totalCases, newCases/newCases],
    ]

    matrix = pd.DataFrame(pairwise_inputs, index=kriteria_data["Kriteria"], columns=kriteria_data["Kriteria"])

    st.markdown("### 🔍 Preview Matriks Perbandingan Kriteria")
    st.dataframe(matrix.style.format("{:.3f}"))

    criteriaComparison = AHPComparison(matrix, kriteria_data["Kriteria"], "Kriteria")

    st.write(f"""
     - Eigen Value: {criteriaComparison.eigenVector:.2f}
     - Consistensi Index(CI): {criteriaComparison.ci:.2f}
     - Consistensi Ratio(CR): {criteriaComparison.cr:.2f}
    """)

    if not criteriaComparison.isConsistent():
        st.warning(f"Pairwase Comparison Criteria: Tidak Konsisten (CR > 0.1)")
    else:
        st.success(f"Pairwase Comparison Criteria: Konsisten (CR <= 0.1)")
        scores = normalizedDataframe @ criteriaComparison.weights
        results_df = pd.DataFrame({
            "Lokasi": cleanDataset.index,
            "Skor AHP": scores
        }).reset_index(drop=True)
        results_df["Rangking"] = results_df["Skor AHP"].rank(ascending=False).astype(int)
        results_df = results_df.sort_values("Rangking")

        st.subheader("🏆 Hasil Perangkingan Alternatif")
        st.dataframe(results_df, use_container_width=True)

        fig = px.bar(results_df, x="Lokasi", y="Skor AHP", color="Rangking",
                    title="Skor AHP per Lokasi", text_auto='.2f',
                    color_continuous_scale=px.colors.sequential.Tealgrn)
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Kesimpulan")

        choosedProvince = results_df.sort_values("Skor AHP", ascending=False)["Lokasi"].values[0]

        st.success(f"Provinsi prioritas distribusi vaksin dengan AHP: {choosedProvince}")


st.markdown("---")
st.caption("💡 Proyek Akhir Sistem Pendukung Keputusan - AHP & COVID-19")
