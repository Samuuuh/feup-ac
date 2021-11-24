import configparser
import os
import pandas as pd

from src.preprocessing.utils import read_cleaned_csv, read_preprocessed_csv

from .consts import ModelType
from .logger import Logger

from .prediction.grid_log_regression import grid_log_regression
from .prediction.log_regression import log_regression
from .prediction.tree_classifier import tree_classifier


def set_columns(columns, df: pd.DataFrame) -> pd.DataFrame:
    for col in columns:
        if columns.get(col) == "False" and col in df.columns:
            df = df.drop([col], axis=1)

    return df


def build(parser: configparser.ConfigParser):
    """This function is responsible for building the dataframe of test and train by merging other tables and selecting the chosen attributes.
    Args:
        parser (configparser.ConfigParser): Config file containing which files should be used and which colums are selected.
    """

    Logger.print_info("Getting tables...")

    # Reading all the tables
    loan_dev = read_preprocessed_csv("loan_dev")
    loan_comp = read_preprocessed_csv("loan_comp")
    account = read_preprocessed_csv("account")
    disp = read_preprocessed_csv("disp")
    client = read_cleaned_csv("client")
    loan_merged = []

    # Merging other tables with the loan_dev and loan_comp
    for loan in [loan_dev, loan_comp]:
        df = pd.merge(account, disp, on="account_id", how="inner")                          # Merge account and disp
        df = pd.merge(loan, df, on="account_id", how="left", suffixes=("_acc", "_loan"))    # Merge loan
        df = pd.merge(df, client, on="client_id", how="left", suffixes=("_acc", "_client")) # Merge client
        df = set_columns(parser['attributes'], df)                                          # Remove columns
        loan_merged.append(df)

    return loan_merged


def call_model(parser: configparser.ConfigParser, dev: pd.DataFrame, comp: pd.DataFrame) -> None:
    model = parser['settings']['model']
    debug_mode = eval(parser['settings']['debug'])
    Logger.print_info(f"Calling model {model}...")

    # Call the train models.
    if model == ModelType.LOG_REGRESSION:
        log_regression(dev, comp, debug_mode)
    elif model == ModelType.GRID_LOG_REGRESSION:
        grid_log_regression(dev, comp, debug_mode)
    elif model == ModelType.TREE_CLASSIFIER:
        tree_classifier(dev, comp, debug_mode)
    else:
        Logger.print_err(f"{model} is not a valid model!")



if __name__ == '__main__':
    filepath = os.path.dirname(os.path.abspath(__file__)) + "/configparser.ini"

    if os.path.isfile(filepath):
        parser = configparser.ConfigParser()
        parser.read(filepath)                       # Get's the config file.
        df = build(parser)                          # Builds the dataframe.
        call_model(parser, df[0], df[1])            # Calls the model.
    else:
        Logger.print_err("No config parser in this folder.")
