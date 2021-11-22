import pandas as pd
import os 

def get_x(df: pd.DataFrame) -> None:
    return df.loc[:, df.columns != 'status']

def get_y(df: pd.DataFrame) -> None:
    return df.status

def read_frame(name: str) -> pd.DataFrame:
    currdir = os.path.dirname(__file__)
    return pd.read_csv(f'{currdir}/../data/preprocessed/{name}.csv', sep=';') 

def save_result(loan_id, predicted, filename: str): 
    currdir = os.path.dirname(__file__)
    prediction = pd.DataFrame({'Id': loan_id, 'Predicted': predicted}).set_index('Id')
    prediction.to_csv(f'{currdir}/../data/submission/{filename}.csv')
