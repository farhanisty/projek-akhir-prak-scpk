import pandas as pd
import numpy as np

class AHPComparison:
    def __init__(self, pariwaseComparation, alternatives, label):
        self.pariwaseComparation = pariwaseComparation
        self.alternatives = alternatives
        self.label = label

        self.normalization()

    def normalization(self):
        self.bobot = self.pariwaseComparation.sum(axis=0)
        self.normalizationMatrix = self.pariwaseComparation / self.bobot
        self.weights = self.normalizationMatrix.sum(axis=1) / len(self.alternatives)
        self.ws = self.pariwaseComparation @ self.weights
        self.onePerW = 1 / self.weights
        self.cv = self.ws * self.onePerW
        self.eigenVector = self.cv.mean()
        self.ci = (self.eigenVector - len(self.alternatives)) / (len(self.alternatives) - 1)
        self.ri = self.countRatioIndex(len(self.alternatives))
        self.cr = self.ci / self.ri

    def isConsistent(self):
        return self.cr <= 0.1

    def countRatioIndex(self, ci):
        if ci >= 7:
            return 1.32
        elif ci >= 6:
            return 1.24
        elif ci >= 5:
            return 1.12
        elif ci >= 4:
            return 0.9
        elif ci >= 3:
            return 0.58
        else:
            return 0
