import pandas as pd
import os 
def read_csv(file: str, columns: list = None) -> pd.DataFrame:
    # loads the dataset stored in the .csv file to a variable
    if columns is None:
        return pd.read_csv('data/raw/' + file + '.csv', low_memory=False, sep=";")
    return pd.read_csv('data/raw/' + file + '.csv', usecols=columns, low_memory=False, sep=";")


def write_csv(df: pd.DataFrame, file: str, index: bool = True) -> str:
    return df.to_csv('./data/preprocessed/' + file + '.csv', sep=';', index=index) 

def read_preprocessed_csv(filename: str) -> pd.DataFrame: 
    position =  os.path.dirname(os.path.abspath(__file__)) + "/.."
    return pd.read_csv(position + '/data/preprocessed/' + filename + '.csv', sep=';')


def read_cleaned_csv(filename: str) -> pd.DataFrame:
    position =  os.path.dirname(os.path.abspath(__file__)) + "/.."
    return pd.read_csv(position + '/data/cleaned/' + filename + '.csv', sep=',')
