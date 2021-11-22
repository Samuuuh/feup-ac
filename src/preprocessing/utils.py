import pandas as pd

def read_csv(file: str, columns: list = None) -> pd.DataFrame:
    # loads the dataset stored in the .csv file to a variable
    if columns is None:
        return pd.read_csv('data/raw/' + file + '.csv', low_memory=False, sep=";")
    return pd.read_csv('data/raw/' + file + '.csv', usecols=columns, low_memory=False, sep=";")


def write_csv(df: pd.DataFrame, file: str, index: bool = True) -> str:
    return df.to_csv('./data/preprocessed/' + file + '.csv', sep=';', index=index)