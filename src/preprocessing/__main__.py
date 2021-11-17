from collections.abc import Callable

import numpy as np
import pandas as pd
from numpy import NaN


def read_csv(file: str, columns: list = None) -> pd.DataFrame:
    # loads the dataset stored in the .csv file to a variable
    if columns is None:
        return pd.read_csv('data/raw/' + file + '.csv', low_memory=False, sep=";")
    return pd.read_csv('data/raw/' + file + '.csv', usecols=columns, low_memory=False, sep=";")


def write_csv(df: pd.DataFrame, file: str, index: bool = True) -> str:
    return df.to_csv('./data/preprocessed/' + file + '.csv', sep=';', index=index)


def split_date(name_year: str, name_month: str, name_day: str, column_name: str, df: pd.DataFrame,
               new_column_name: str = None) -> None:
    df[[name_year, name_month, name_day]] = [list(map(''.join, zip(*[iter(str(date))] * 2))) for date in
                                             df[column_name]]
    df[name_year] = df[name_year].astype('int') + 1900
    df[name_month] = df[name_month].astype('int')
    df[name_day] = df[name_day].astype('int')
    del df[column_name]

    if new_column_name is not None:
        join_date(name_year, name_month, name_day, new_column_name, df)


def join_date(name_year: str, name_month: str, name_day: str, column_name: str, df: pd.DataFrame) -> None:
    df[column_name] = (df[name_year].astype('str') + '-' + df[name_month].astype('str') + '-' +
                       df[name_day].astype('str'))
    df[column_name] = pd.to_datetime(df[column_name])


def preprocess(file_name: str, parse_function: Callable[[pd.DataFrame], [pd.DataFrame]]):
    df = read_csv(file_name)
    df = parse_function(df)
    write_csv(df, file_name, index=False)


def read_account() -> None:
    def parse_data(df: pd.DataFrame) -> pd.DataFrame:
        split_date("creation_year", "creation_month", "creation_day", "date", df, "creation_date")
        return df

    preprocess("account", parse_data)


def read_card() -> None:
    def parse_data(df: pd.DataFrame) -> pd.DataFrame:
        split_date("issued_year", "issued_month", "issued_day", "issued", df, "issued_date")
        return df

    preprocess("card_dev", parse_data)
    preprocess("card_comp", parse_data)


def read_client() -> None:
    def parse_data(df: pd.DataFrame) -> pd.DataFrame:
        # Separating the birth number into day, month and year
        df.birth_number = df.birth_number.astype('str')
        df["birthdate_year"] = 1900 + df.birth_number.str[:2].astype('int')
        df["birthdate_month"] = df.birth_number.str[2:4].astype('int')
        df["birthdate_day"] = df.birth_number.str[4:].astype('int')

        # The month was added by 50 for women, we are going to revert that and add a sex attribute
        df["sex"] = np.where(df.birthdate_month > 12, 'f', 'm')
        df.loc[df.sex == 'f', "birthdate_month"] = df.birthdate_month - 50

        # Creating a birthdate column as a datetime
        join_date("birthdate_year", "birthdate_month", "birthdate_day", "birthdate", df)

        # Removing the now useless column birth_number
        return df.drop(columns=["birth_number"])

    preprocess("client", parse_data)


def read_disposition() -> None:
    def parse_data(df: pd.DataFrame) -> pd.DataFrame:
        # Changing the types to be in small letters like the other categorical attributes that are not codes
        df.type = np.where(df.type == "OWNER", 'owner', 'disponent')

        return df

    preprocess("disp", parse_data)


def read_district() -> None:
    def parse_data(df: pd.DataFrame) -> pd.DataFrame:
        # Region direction and Region
        df['region_direction'] = df['region'].apply(lambda x: x.split(" ")[0] if x.find(" ") != -1 else pd.NA)
        df['region'] = df['region'].apply(lambda x: x.split(" ")[1] if x.find(" ") != -1 else x)

        # Split name
        df['city_area'] = df['name'].apply(lambda x: x.split(" - ")[1] if x.find(" - ") != -1 else pd.NA)
        df['city'] = df['name'].apply(lambda x: x.split(" - ")[0] if x.find(" - ") != -1 else x)

        del df['name']
        del df['city_area']  # Not much information after analysis.

        df = df.rename({
            'no. of inhabitants': 'num_inhab',
            'no. of cities ': 'num_cities',
            'ratio of urban inhabitants ': 'perc_urban_inhab',
            'no. of commited crimes \'96 ': 'num_crimes_96',
            'no. of commited crimes \'95 ': 'num_crimes_95',
            'unemploymant rate \'96 ': 'perc_unemploy_96',
            'unemploymant rate \'95 ': 'perc_unemploy_95',
            'average salary ': 'avg_salary',
            'code': 'id',
            'no. of enterpreneurs per 1000 inhabitants ': 'enterp_per_1000',
            'no. of municipalities with inhabitants < 499 ': 'num_municip_inhab_0_499',
            'no. of municipalities with inhabitants 500-1999': 'num_municip_inhab_500_1999',
            'no. of municipalities with inhabitants 2000-9999 ': 'num_municip_inhab_2000_9999',
            'no. of municipalities with inhabitants >10000 ': 'num_municip_inhab_10000_'
        }, axis=1)
        return df

    preprocess("district", parse_data)


def read_loan() -> None:
    def parse_data(df: pd.DataFrame) -> pd.DataFrame:
        split_date("loan_year", "loan_month", "loan_day", "date", df, "loan_date")
        return df

    preprocess("loan_dev", parse_data)
    preprocess("loan_comp", parse_data)


def read_transaction() -> None:
    def parse_data(df: pd.DataFrame) -> pd.DataFrame:
        # Create a column for each date segment and creating a date attribute
        split_date("trans_year", "trans_month", "trans_day", "date", df, "trans_date")

        # Removing information about the operation from the type
        df.loc[df.type == 'withdrawal in cash', "type"] = 'withdrawal'

        # Removing information about the type from the operation
        # obs: all transactions that have null operations are of the credit type
        conditions = [df.operation == 'credit in cash', df.operation == 'withdrawal in cash',
                      df.operation == 'collection from another bank', df.operation == 'remittance to another bank',
                      df.operation == 'credit card withdrawal', df.operation.isna()]
        values = ['cash', 'cash', 'another bank', 'another bank', 'credit card', NaN]
        df.operation = np.select(conditions, values)

        # Joining the empty k_symbol with the NaN
        df.loc[df.k_symbol == ' ', "k_symbol"] = NaN

        return df

    preprocess("trans_dev", parse_data)
    preprocess("trans_comp", parse_data)


if __name__ == "__main__":
    read_account()
    read_card()
    read_client()
    read_disposition()
    read_district()
    read_loan()
    read_transaction()
