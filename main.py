import streamlit as st
from DatasetProcessor import DatasetProcessor

st.title("COVID-19 Dataset")

st.subheader("Deskripsi Dataset")
st.markdown("""
    <p style='text-align: justify'>
    Program ini kami buat menggunakan metode AHP yang memiliki tujuan untuk membantu pemerintah dalam memantau dan menganalisis data COVID-19 secara efektif. 
    Melalui aplikasi ini, pemerintah dapat mengakses data mentah, menyaring informasi terbaru dalam 2 bulan terakhir, 
    melihat data penting seperti jumlah kasus, kematian, dan kepadatan penduduk, serta mengelompokkan data berdasarkan 
    provinsi. Selain itu, analisis dengan metode AHP memungkinkan penentuan prioritas wilayah yang memerlukan intervensi 
    lebih lanjut, seperti distribusi vaksin atau pengetatan kebijakan. Program ini juga mendukung transparansi data dan 
    fleksibilitas pengembangan lebih lanjut untuk analisis terpadu.
    </p>
    <br>
    <p style='text-align: justify'>
    Dataset ini berisi data perkembangan COVID-19 di Indonesia dari berbagai provinsi.
    Data mencakup informasi seperti:
    
    - **Tanggal** laporan
    - **Provinsi** tempat data dikumpulkan
    - **Jumlah Kasus Baru**, **Meninggal**, **Sembuh**, dan **Kasus Aktif Baru**
    - **Total Kasus**, **Total Meninggal**, **Total Sembuh**, dan **Kasus Aktif Total**
    - **Kepadatan Penduduk**
    - **Koordinat Lokasi** (Longitude & Latitude)
    - **Tingkat Kematian dan Kesembuhan** dalam persentase
    </p>
    """, unsafe_allow_html=True)

st.subheader("Berikut Dataset yang kami peroleh : ")
datasetProcessor = DatasetProcessor("dataset/data_covid.csv")

st.subheader("📄 Dataset Mentah")
st.dataframe(datasetProcessor.pandasDataset)

st.subheader("📆 Dataset 2 Bulan Terakhir")
st.dataframe(datasetProcessor.pandasDatasetTowLatestMonth)

st.subheader("📊 Dataset Kolom Terpilih")
st.dataframe(datasetProcessor.pandasDatasetFilteredByUsedColumns)

st.subheader("📍 Dataset tanpa Lokasi 'Indonesia'")
st.dataframe(datasetProcessor.pandasDatasetNotIncludeIndonesiaLocation)

st.subheader("📌 Dataset dikelompokkan per Provinsi")
st.dataframe(datasetProcessor.pandasDatasetGroupedByLocation)
