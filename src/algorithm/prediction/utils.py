import pandas as pd
import matplotlib.pyplot as plt
import pickle

def get_x(df: pd.DataFrame) -> None:
    condition = (df.columns != 'status') & (df.columns != 'account_id') & (df.columns != 'loan_id') & (
        df.columns != 'client_id') & (df.columns != 'district_id') & (df.columns != 'disp_id') & (df.columns != 'district_id_y') & (
        df.columns != 'district_id_x') & (df.columns != 'id')
    return df.loc[:, condition]


def get_y(df: pd.DataFrame) -> None:
    return df.status


def save_result(loan_id, predicted, filename: str):
    prediction = pd.DataFrame({'Id': loan_id, 'Predicted': predicted}).set_index('Id')
    prediction.to_csv(f'data/submission/{filename}.csv')


def print_feature_importance(importance, col_names):
    plt.bar(col_names, height= importance.ravel())
    plt.xticks(rotation=45, ha="right")
    plt.show()

def save_model(model, filename):
    pickle.dump(model, open(f'data/models/{filename}.sav', "wb"))

def read_model(filename):
    return pickle.load(open(f'data/models/{filename}.sav', "rb"))
