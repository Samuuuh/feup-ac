import configparser
import os
import pandas as pd
import sys

from src.prediction.k_means import k_means
from src.prediction.random_forest import random_forest
from src.prediction.random_forest_smote import random_forest_smote
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

    disp = read_cleaned_csv("disp")
    client = read_cleaned_csv("client")
    card = read_cleaned_csv("card")

    # Reading all the tables
    loan_dev = read_preprocessed_csv("loan_dev")
    loan_comp = read_preprocessed_csv("loan_comp")

    trans_comp = read_cleaned_csv("trans_comp")
    trans_dev = read_cleaned_csv("trans_dev")

    account = read_preprocessed_csv("account")
    loan_merged = []

    # Merging other tables with the loan_dev and loan_comp
    for i, loan in enumerate([loan_dev, loan_comp]):

        df = pd.merge(loan, account, on="account_id", how="left",
                      suffixes=("_acc", "_loan"))    # Merge loan
        df = pd.merge(df, disp, on='account_id', how="inner")
        df = pd.merge(df, client, on="client_id", how="inner")
        df = pd.merge(df, card, on="disp_id", how="left")
        if i == 0:
            df = pd.merge(df, trans_dev, on="account_id", how="inner")
        else:
            df = pd.merge(df, trans_comp, on="account_id", how="inner")

        # Remove columns
        df = set_columns(parser['attributes'], df)
        loan_merged.append(df)
    return loan_merged


def call_model(parser: configparser.ConfigParser, dev: pd.DataFrame, comp: pd.DataFrame) -> None:
    model = parser['settings']['model']
    debug_mode = eval(parser['settings']['debug'])
    Logger.print_info(f"Calling model {model}...")

    # Call the train models.
    if model == ModelType.K_MEANS:
        k_means(dev, comp, debug_mode)
    elif model == ModelType.LOG_REGRESSION:
        log_regression(dev, comp, debug_mode)
    elif model == ModelType.GRID_LOG_REGRESSION:
        grid_log_regression(dev, comp, debug_mode)
    elif model == ModelType.TREE_CLASSIFIER:
        tree_classifier(dev, comp, debug_mode)
    elif model == ModelType.RANDOM_FOREST:
        random_forest(dev, comp, debug_mode)
    elif model == ModelType.RANDOM_FOREST_SMOTE:
        random_forest_smote(dev, comp, debug_mode)
    else:
        Logger.print_err(f"{model} is not a valid model!")


def convert_status(df: pd.DataFrame):
    """ This function is responsible for changing the status in the following format:
    -1 -> 1
    1 -> 0
    """
    df['status'] = df['status'].replace([1, -1], [0, 1])
    return df


if __name__ == '__main__':
    if len(sys.argv) < 2:
        path = "/../config/config.ini"
    else:
        path = "/../" + sys.argv[1]
    filepath = os.path.dirname(os.path.abspath(__file__)) + path

    if os.path.isfile(filepath):
        parser = configparser.ConfigParser()
        parser.read(filepath)                       # Get's the config file.
        df = build(parser)                          # Builds the dataframe.
        df[0] = convert_status(df[0])
        call_model(parser, df[0], df[1])            # Calls the model.
    else:
        Logger.print_err("No config parser in this folder.")
