from DatasetProcessor import DatasetProcessor
import numpy as np
import pandas as pd
from DatasetProcessor import DatasetProcessor
from AHPComparison import AHPComparison

datasetProcessor = DatasetProcessor("dataset/data_covid.csv")

# langkah setiap prosess data
print(datasetProcessor.pandasDataset)
print(datasetProcessor.pandasDatasetTowLatestMonth)
print(datasetProcessor.pandasDatasetFilteredByUsedColumns)
print(datasetProcessor.pandasDatasetNotIncludeIndonesiaLocation)
print(datasetProcessor.pandasDatasetGroupedByLocation)
print(datasetProcessor.pandasDataset)


# fungsi buat normalisasi dataframe, alternatif tidak perlu pairwase cukup di normalisasi pake fungsi ini
def normalize_dataframe(df, criteria_types):
    df_norm = df.copy().astype(float)

    for i, column in enumerate(df.columns):
        if criteria_types[i]:  # Benefit
            df_norm[column] = df[column] / df[column].max()
        else:  # Cost
            df_norm[column] = df[column].min() / df[column]
    
    return df_norm

# objek buat prosess data, setiap prosess nanti tampilkan
datasetProcessor = DatasetProcessor("dataset/data_covid.csv")

# dataset yang udah clean disini cleanDataset = datasetProcessor.pandasDatasetGroupedByLocation

# bikin pake slider perbandingannya
criteriaComparison = AHPComparison(np.array([
    [1, 2, 3, 4, 5],
    [1 / 2, 1, 1, 1, 1],
    [1 / 3, 1, 1, 1, 1],
    [1 / 4, 1, 1, 1, 1],
    [1 / 5, 1, 1, 1, 1],
]), cleanDataset.columns, "Kriteria")

# normalisasi dataset
normalizedDataset = normalize_dataframe(cleanDataset, [True, False, True, True, True])

# perkalian matriks buat dapat perangkingan alternatif
perangkinganAlternative = normalizedDataset @ criteriaComparison.weights

# mengubah perangkinganAlternative yang sebelumnya bentuknya series jadi dataframe biar bisa ditambahin kolom rangking
dataframe = pd.DataFrame({
    "Skor AHP": perangkinganAlternative
})

# nambahin kolom rangking
dataframe["Rangking"] = dataframe["Skor AHP"].rank(ascending=False).astype(int)

# ambil hasilnya
print(dataframe.idxmax(axis=0)["Skor AHP"])
