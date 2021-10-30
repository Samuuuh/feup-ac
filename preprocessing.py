from numpy import NaN
import numpy as np
import pandas as pd


def read_csv(file: str, columns: list = None):
    # loads the dataset stored in the .csv file to a variable
    if columns is None:
        return pd.read_csv('docs/' + file + '.csv', low_memory=False, sep=";")
    return pd.read_csv('docs/' + file + '.csv', usecols=columns, low_memory=False, sep=";")


def write_csv(df: pd.DataFrame, file: str, index: bool = True):
    return df.to_csv('./preprocessing/' + file + '.csv', sep=';', index=index)


def split_date(name_year: str, name_month: str, name_day: str, column_name: str, df: pd.DataFrame) -> None:
    df[[name_year, name_month, name_day]] = [list(map(''.join, zip(*[iter(str(date))] * 2))) for date in
                                             df[column_name]]
    del df[column_name]


def read_account():
    df = read_csv("account", ["account_id", "district_id", "frequency", "date"])

    # Split Date into year, month and day
    split_date("creation_year", "creation_month", "creation_day", "date", df)

    write_csv(df, "account")


def read_loan_train():
    df = read_csv("loan_train", ["loan_id", "account_id", "date", "amount", "duration", "payments", "status"])

    # Split Date into year, month and day
    split_date("loan_year", "loan_month", "loan_day", "date", df)

    write_csv(df, "loan_train")

    df = read_csv("loan_test", ["loan_id", "account_id", "date", "amount", "duration", "payments", "status"])

    # Split Date into year, month and day
    split_date("loan_year", "loan_month", "loan_day", "date", df)

    write_csv(df, "loan_test")


def read_card_train():
    df = read_csv("card_train")
    split_date("issued_year", "issued_month", "issued_day", "issued", df)
    write_csv(df, "card_train", index=False)


def read_district():
    df = read_csv("district")

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

    write_csv(df, "district", index=False)


def read_client():
    def parse_data(df: pd.DataFrame):
        # Separating the birth number into day, month and year
        df.birth_number = df.birth_number.astype('str')
        df["birthdate_year"] = 1900 + df.birth_number.str[:2].astype('int')
        df["birthdate_month"] = df.birth_number.str[2:4].astype('int')
        df["birthdate_day"] = df.birth_number.str[4:].astype('int')

        # The month was added by 50 for women, we are going to revert that and add a sex attribute
        df["sex"] = np.where(df.birthdate_month > 12, 'f', 'm')
        df.loc[df.sex == 'f', "birthdate_month"] = df.birthdate_month - 50

        # Creating a birthdate column as a datetime
        df["birthdate"] = (df.birthdate_year.astype('str') + '-' + df.birthdate_month.astype('str') + '-' +
                           df.birthdate_day.astype('str'))
        df.birthdate = pd.to_datetime(df.birthdate)

        # Removing the now useless column birth_number
        return df.drop(columns=["birth_number"])

    clients = read_csv("client")
    clients = parse_data(clients)
    write_csv(clients, "client", index=False)


if __name__ == "__main__":
    read_account()
    read_loan_train()
    read_card_train()
    read_district()
    read_client()
