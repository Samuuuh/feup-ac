import pandas as pd
import os


def get_x(df: pd.DataFrame) -> None:
    condition = (df.columns != 'status') & (df.columns != 'account_id') & (df.columns != 'loan_id') & (
        df.columns != 'client_id') & (df.columns != 'district_id') & (df.columns != 'disp_id')
    return df.loc[:, condition]


def get_y(df: pd.DataFrame) -> None:
    return df.status


def save_result(loan_id, predicted, filename: str):
    currdir = os.path.dirname(__file__)
    prediction = pd.DataFrame({'Id': loan_id, 'Predicted': predicted}).set_index('Id')
    prediction.to_csv(f'{currdir}/../data/submission/{filename}.csv')
