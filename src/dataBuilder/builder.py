from abc import abstractmethod
import pandas as pd
import os
import sys
from logger import Logger
sys.path.append("..") # Adds higher directory to python modules path.

class Builder:

    def read_frame(self, name: str) -> pd.DataFrame:
            position =  os.path.dirname(os.path.abspath(__file__)) + "/.."
            return pd.read_csv(position + '/data/preprocessed/' + name + '.csv', sep=';')

    # Remove not selected columns
    def drop_column(self, col: str):
        if self.columns.get(col) == "False" and col in self.df.columns: 
            self.df = self.df.drop([col], axis=1) 

    @abstractmethod
    def handle_creation(self, col: str): 
        Logger.print_err("handle_creation not implemented")

    @abstractmethod
    def set_columns(self):
        Logger.print_err("set_columns not implemented")