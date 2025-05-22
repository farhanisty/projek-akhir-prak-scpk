import pandas
from datetime import datetime
from dateutil.relativedelta import relativedelta


class DatasetProcessor:
    def __init__(self, datasetPath):
        self.datasetPath = datasetPath
        self.pandasDataset = pandas.read_csv(datasetPath)
        self.processDataset()
        

    def processDataset(self):
        self.processTwoLatestMonthDataset()
        self.processFilterUsedColumns()
        self.processRemoveWhereLocationIndonesia()
        self.processGroupDatasetByLocation()

    def processTwoLatestMonthDataset(self):
        self.pandasDatasetTowLatestMonth = self.pandasDataset
        self.pandasDatasetTowLatestMonth["Date"] = pandas.to_datetime(self.pandasDatasetTowLatestMonth['Date'], errors="coerce")
        self.pandasDatasetTowLatestMonth = self.pandasDatasetTowLatestMonth.dropna(subset=["Date"])
        bulan_terbaru = self.pandasDatasetTowLatestMonth['Date'].dt.to_period('M').drop_duplicates().sort_values(ascending=False).head(2)
        self.pandasDatasetTowLatestMonth = self.pandasDatasetTowLatestMonth[self.pandasDatasetTowLatestMonth['Date'].dt.to_period('M').isin(bulan_terbaru)]

    def processFilterUsedColumns(self):
        self.pandasDatasetFilteredByUsedColumns = self.pandasDatasetTowLatestMonth[['Date', 'Location', 'Population Density', 'Total Recovered', 'Total Deaths', 'Total Cases', 'New Cases']]

    def processRemoveWhereLocationIndonesia(self):
        self.pandasDatasetNotIncludeIndonesiaLocation = self.pandasDatasetFilteredByUsedColumns[~self.pandasDatasetFilteredByUsedColumns['Location'].str.lower().eq('indonesia')]

    def processGroupDatasetByLocation(self):
        self.pandasDatasetGroupedByLocation = self.pandasDatasetNotIncludeIndonesiaLocation.groupby('Location').agg({
            'Population Density': 'max',
            'Total Recovered': 'max',
            'Total Deaths': 'max',
            'Total Cases': 'max',
            'New Cases': 'sum'
        })
