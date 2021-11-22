import configparser
import os
import pandas as pd

from .dataBuilder.loan_builder import LoanBuilder
from .consts import ModelType
from .logger import Logger

from .prediction.grid_log_regression import grid_log_regression
from .prediction.log_regression import log_regression


def build(parser: configparser.ConfigParser) -> LoanBuilder:
    """This function is responsible for building the dataframe of test and train. 
    Args:
        parser (configparser.ConfigParser): Config file containing which files should be used and which colums are selected.
    """

    Logger.print_info("Generating tables...")
    tables = parser['selected tables']
    loan_builder = LoanBuilder(parser['loan'])

    # Merge the tables with loan builder.
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

    return loan_builder

def call_model(parser: configparser.ConfigParser, loan_builder: LoanBuilder) -> None:
    model = parser['settings']['model']
    debug_mode = eval(parser['settings']['debug']) 
    comp = loan_builder.df_comp
    dev = loan_builder.df_dev
    Logger.print_info(f"Calling model {model}...")  

    # Call the train models.
    if model == ModelType.LOG_REGRESSION: 
        log_regression(dev, comp, debug_mode) 
    elif model == ModelType.GRID_LOG_REGRESSION:
        grid_log_regression(dev, comp, debug_mode)
    else: 
        Logger.print_err(f"{model} is not a valid model!")
    

if __name__ == '__main__':
    filepath = os.path.dirname(os.path.abspath(__file__)) + "/configparser.ini" 

    if os.path.isfile(filepath):
        parser = configparser.ConfigParser()
        parser.read(filepath)                       # Get's the config file.
        loan_builder = build(parser)                # Builds the dataframe.
        call_model(parser, loan_builder)            # Calls the model.
    else:
        Logger.print_err("No config parser in this folder.")
