import streamlit as st
import pandas as pd


@st.cache_data
def load_data():
    df = pd.read_csv("Data_COVID19_Indonesia.csv", parse_dates=['Date'], dayfirst=True, infer_datetime_format=True)
    return df

df = load_data()


st.title("COVID-19 Indonesia Data Viewer")
tab1, tab2, tab3, tab4 = st.tabs(["Raw Dataset", "Filtered Data (Last 2 Months)", "Grouped by Province", "AHP Results"])

with tab1:
    st.subheader("Deskripsi Dataset")
    st.markdown("""
    Dataset ini berisi data perkembangan COVID-19 di Indonesia dari berbagai provinsi.
    Data mencakup informasi harian seperti:

    - **Tanggal** laporan
    - **Provinsi** tempat data dikumpulkan
    - **Jumlah Kasus Baru**, **Meninggal**, **Sembuh**, dan **Kasus Aktif Baru**
    - **Total Kasus**, **Total Meninggal**, **Total Sembuh**, dan **Kasus Aktif Total**
    - **Kepadatan Penduduk**
    - **Koordinat Lokasi** (Longitude & Latitude)
    - **Tingkat Kematian dan Kesembuhan** dalam persentase

    Dataset ini digunakan untuk analisis penyebaran, pengelompokan, dan penilaian risiko berdasarkan metode AHP.
    """)

    st.subheader("Raw Dataset (first 100 rows)")
    st.dataframe(df.head(100))

with tab2:
    st.subheader("Filtered Data (Last 2 Months)")
    latest_date = df['Date'].max()
    two_months_ago = latest_date - pd.DateOffset(months=2)
    filtered_df = df[(df['Date'] >= two_months_ago) & (df['Date'] <= latest_date)]
    selected_cols = ['Population Density', 'Total Recovered', 'Total Deaths', 'Total Cases', 'New Active Cases']
    st.dataframe(filtered_df[selected_cols].head(100))

with tab3:
    st.subheader("Grouped by Province (Average Values)")
    grouped_df = df.dropna(subset=['Province']).groupby('Province')[
        ['Total Cases', 'Total Deaths', 'Total Recovered', 'New Active Cases', 'Population Density']
    ].mean().reset_index()
    st.dataframe(grouped_df)

with tab4:
    st.subheader("AHP Results (Simplified)")
    ahp_df = grouped_df.copy()
    ahp_df['AHP Score'] = ahp_df[['Total Cases', 'Total Deaths', 'New Active Cases']].mean(axis=1)
    ahp_df = ahp_df.sort_values(by='AHP Score', ascending=False)
    st.dataframe(ahp_df)
