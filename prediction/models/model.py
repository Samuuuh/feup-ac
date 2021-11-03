from abc import ABC, abstractmethod

import pandas as pd


class Model(ABC):

    @abstractmethod
    def train(self, dataframe: pd.DataFrame) -> None:
        pass

    @abstractmethod
    def test(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        pass

    def score(self, expected: pd.DataFrame, predicted: pd.DataFrame) -> float:
        return 0
