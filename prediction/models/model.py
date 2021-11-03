from abc import ABC, abstractmethod

import pandas as pd


class Model(ABC):

    @abstractmethod
    def train(self, dataframe: pd.DataFrame) -> None:
        pass

    @abstractmethod
    def test(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        pass

    @staticmethod
    def get_prediction(dataframe: pd.DataFrame, id_column: str, goal_column: str) -> pd.DataFrame:
        expected = dataframe[[id_column, goal_column]]
        expected = expected.rename(columns={id_column: "Id", goal_column: "Predicted"})
        return expected.set_index('Id')

    def score(self, expected: pd.DataFrame, predicted: pd.DataFrame) -> float:
        # TODO: implement AUC for the two dataframes
        return 0
