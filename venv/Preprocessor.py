import pandas as pd
import numpy as np

class Preprocessor:

    def __init__(self, df):
        self.df = df
        self.fillMissingValues_standardization()
        self.groupByCountry()

    def fillMissingValues_standardization(self):
        #replace missing value with column mean
        for column in self.df:
            if column != 'country' and column != 'year':
                self.df[column].fillna(self.df[column].mean(), inplace=True)
                self.df[column] = self.df[column].apply(
                    lambda val: (val - self.df[column].mean()) / self.df[column].std())


    def groupByCountry(self):
        self.df = self.df.groupby("country").mean()
        self.df = self.df.drop(["year"], axis=1)
