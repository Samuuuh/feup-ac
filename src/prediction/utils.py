import pandas as pd

def get_x(df: pd.DataFrame) -> None:
    return df.loc[:, df.columns != 'status']

def get_y(df: pd.DataFrame) -> None:
    return df.status

def read_frame(name: str) -> pd.DataFrame:
    return pd.read_csv('./data/preprocessed/' + name + '.csv', sep=';')