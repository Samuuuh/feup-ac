import configparser
import os
from logger import Logger
from dataBuilder.loan_builder import LoanBuilder


def build(parser: configparser.ConfigParser):
    tables = parser['Selected Tables']
    df = LoanBuilder(parser['loan']).df
    print(df.head())


if __name__ == '__main__':
    filepath = os.path.dirname(os.path.abspath(__file__)) + "/configparser.ini" 

    if os.path.isfile(filepath):
        parser = configparser.ConfigParser()
        parser.read(filepath)
        build(parser)
    else:
        Logger.print_err("No config parser in this folder.")


