from abc import ABC, abstractmethod

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class Model(ABC):

    def __init__(self):
        self.area = None
        self.score_dataframe = None

    @abstractmethod
    def train(self, dataframe: pd.DataFrame) -> None:
        pass

    @abstractmethod
    def test(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        pass

    @staticmethod
    def get_expected(dataframe: pd.DataFrame, id_column: str, goal_column: str) -> pd.DataFrame:
        expected = dataframe[[id_column, goal_column]]
        expected = expected.rename(columns={id_column: "Id", goal_column: "Expected"})
        return expected.set_index('Id')

    def plot_roc(self):
        plt.plot(self.score_dataframe['sensibility'], self.score_dataframe['one_minus_specificity'])
        plt.show()

    def score(self, expected: pd.DataFrame, predicted: pd.DataFrame) -> float:
        if self.area is not None:
            return self.area

        dataframe = predicted.join(expected, on='Id')
        ordered = dataframe.sort_values(by='Predicted', ascending=False)

        yes_len = len(ordered.loc[ordered.Expected == 1].index)
        no_len = len(ordered.loc[ordered.Expected != 1].index)

        # Create temporary columns
        ordered['yes'] = np.where(ordered.Expected == 1, 1, 0)
        ordered['no'] = np.where(ordered.Expected != 1, 1, 0)
        ordered['yes_sum'] = ordered.yes.cumsum()
        ordered['no_sum'] = ordered.no.cumsum()

        # Create the columns for sensibility and 1 - specificity
        ordered['sensibility'] = ordered.yes_sum / yes_len
        ordered['one_minus_specificity'] = ordered.no_sum / no_len

        # Remove temporary columns
        ordered = ordered.drop(columns=['yes', 'no', 'yes_sum', 'no_sum'])
        self.score_dataframe = ordered

        # Calculate the area under the ROC using the trapezoidal rule
        self.area = np.trapz(ordered['one_minus_specificity'], ordered['sensibility'])
        return self.area
