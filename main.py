import streamlit as st
from DatasetProcessor import DatasetProcessor

st.title("COVID-19 Dataset Viewer")

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
