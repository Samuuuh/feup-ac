import pandas as pd
import os
import configparser

from dataBuilder.builder import Builder
from logger import Logger
import sys
sys.path.append("..") # Adds higher directory to python modules path.


class LoanBuilder(Builder):
    def __init__(self, columns: configparser.SectionProxy):
        Logger.print_info("Generating loan...")
        self.columns = columns
        self.df = self.read_frame("loan_dev")
        self.set_columns()
        Logger.print_suc("Generated loan")

    def set_columns(self):
        for col in self.columns:
            self.drop_column(col)
            self.handle_creation(col)
    
    def handle_creation(self, col: str): 
        if  self.columns.get(col) == "True" and col not in self.df.columns:
            Logger.print_wrn(f"loan still can't generate \"{col}\"")

   