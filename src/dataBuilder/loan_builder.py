import pandas as pd
import configparser
import sys
from .builder import Builder
from ..logger import Logger


class LoanBuilder(Builder):
    def __init__(self, columns: configparser.SectionProxy):
        Logger.print_info("Generating loan...")
        self.columns = columns
        self.df_dev = self.read_frame("loan_dev")
        self.df_comp = self.read_frame("loan_comp")

        self.set_columns()
        Logger.print_suc("Generated loan")


    def set_columns(self):
        for col in self.columns:
            self.df_dev = self.drop_column(col, self.df_dev)
            self.df_dev = self.handle_creation(col, self.df_dev)

            self.df_comp = self.drop_column(col, self.df_comp)
            self.df_comp = self.handle_creation(col, self.df_comp)


    def handle_creation(self, col: str, df: pd.DataFrame) -> pd.DataFrame:
        if self.columns.get(col) == "True" and col not in df.columns:
            Logger.print_wrn(f"loan still can't generate \"{col}\"")
        return df
