from abc import ABC, abstractmethod

import numpy as np
import pandas as pd


class Model(ABC):

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

    def score(self, expected: pd.DataFrame, predicted: pd.DataFrame) -> float:
        # TODO: implement AUC for the two dataframes
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

        print(ordered)


        return 0
