import configparser
import os
import pandas as pd
import sys

from ..consts import ModelType
from ..logger import Logger
from ...preprocessing.utils import read_cleaned_csv, read_preprocessed_csv
from ..__main__ import build, convert_status
from .k_means import k_means
from .affinity import affinity
from .k_means_tunning import k_means_tunning

import sqlite3

if __name__ == '__main__':
    if len(sys.argv) < 2:
        path = "/../../../config/config.ini"
    else:
        path = "/../../../" + sys.argv[1]
    filepath = os.path.dirname(os.path.abspath(__file__)) + path

    if os.path.isfile(filepath):
        parser = configparser.ConfigParser()
        parser.read(filepath)                       # Get's the config file.
        df = build(parser)                          # Builds the dataframe.
        df[0] = convert_status(df[0])
        affinity(df)
        #k_means_tunning(df)
    else:
        Logger.print_err("No config parser in this folder.")
