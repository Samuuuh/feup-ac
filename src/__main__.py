import configparser
import os
import pandas as pd

from dataBuilder.loan_builder import LoanBuilder
from consts import ModelType
from logger import Logger
from prediction.__main__ import *

def build(parser: configparser.ConfigParser):
    Logger.print_info("Generating tables...")
    tables = parser['selected tables']
    df = LoanBuilder(parser['loan']).df

    if tables['account'] == 'True':
        Logger.print_wrn("Account still not implemented")
    if tables['card'] == 'True':
        Logger.print_wrn("Card still not implemented")
    if tables['client'] == 'True':
        Logger.print_wrn("Client still not implemented")
    if tables['disposition'] == 'True':
        Logger.print_wrn("Disposition still not implemented")
    if tables['transactions'] == 'True':
        Logger.print_wrn("Transactions till not implemented")

    return df

def call_model(parser: configparser.ConfigParser, df: pd.DataFrame) -> None:
    model = parser['settings']['model']
    Logger.print_info(f"Calling model {model}...")  
    if model == ModelType.LOG_REGRESSION:
        simple(df)
    else: 
        Logger.print_err(f"{model} is not a valid model!")
    



if __name__ == '__main__':
    filepath = os.path.dirname(os.path.abspath(__file__)) + "/configparser.ini"

    if os.path.isfile(filepath):
        parser = configparser.ConfigParser()
        parser.read(filepath)
        df = build(parser)
        call_model(parser, df)
    else:
        Logger.print_err("No config parser in this folder.")
