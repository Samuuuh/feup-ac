import configparser
import os
import pandas as pd
import sys

from .consts import ModelType
from .logger import Logger
from .prediction.k_means import k_means
from .prediction.grid_log_regression import grid_log_regression
from .prediction.log_regression import log_regression
from .prediction.neural_networks import neural_network_smote
from .prediction.random_forest import random_forest
from .prediction.random_forest_smote import random_forest_smote
from .prediction.tree_classifier import tree_classifier
from .preprocessing.utils import read_cleaned_csv, read_preprocessed_csv

import sqlite3

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
    db_dev = './data/ac-dev_v-1.db'
    db_comp  = './data/ac-comp_v-1.db'
    connec_dev = sqlite3.connect(db_dev)
    connec_comp = sqlite3.connect(db_comp)

    # -- Get Collumns
    account = pd.read_sql_query("SELECT * FROM account", connec_dev)

    card_dev = pd.read_sql_query("SELECT * FROM card", connec_dev)
    card_comp = pd.read_sql_query("SELECT * FROM card", connec_comp)

    client = pd.read_sql_query("SELECT * FROM client", connec_dev)
    disp = pd.read_sql_query("SELECT * FROM disp", connec_dev)
    district = pd.read_sql_query("SELECT * FROM district", connec_dev)

    loan_dev = pd.read_sql_query("SELECT * FROM loan", connec_dev)
    loan_comp = pd.read_sql_query("SELECT * FROM loan", connec_comp)

    trans_comp = read_cleaned_csv("trans_comp")
    trans_dev = read_cleaned_csv("trans_dev")

    # --- Merge Everythings
    features_dev = 0
    features_comp = 0

    exit(-1)

    return [features_dev, features_comp]


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
    elif model == ModelType.NEURAL_NETWORK_SMOTE:
        neural_network_smote(dev, comp, debug_mode)
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
