import pandas as pd
import os
import configparser

from dataBuilder.builder import Builder

class LoanBuilder(Builder):
    def __init__(self, columns: configparser.SectionProxy):
        self.columns = columns
        self.df = self.read_frame("loan_dev")
        self.remove_columns()

    # Remove not selected columns
    def remove_columns(self):
        for key in self.columns:
            if self.columns.get(key) == "False": 
                self.df = self.df.drop([key], axis=1)


   