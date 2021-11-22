from abc import abstractmethod
import pandas as pd
import os
from ..logger import Logger

class Builder:

    def read_frame(self, name: str) -> pd.DataFrame:
            position =  os.path.dirname(os.path.abspath(__file__)) + "/.."
            return pd.read_csv(position + '/data/preprocessed/' + name + '.csv', sep=';')

    # Remove not selected columns
    def drop_column(self, col: str, df: pd.DataFrame) -> pd.DataFrame:
        if self.columns.get(col) == "False" and col in df.columns: 
            df = df.drop([col], axis=1) 
        return df

    @abstractmethod
    def handle_creation(self, col: str, df: pd.DataFrame) -> pd.DataFrame: 
        Logger.print_err("handle_creation not implemented")

    @abstractmethod
    def set_columns(self):
        Logger.print_err("set_columns not implemented")