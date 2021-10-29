from numpy import NaN
import numpy as np
import pandas as pd

def read_csv(file):
    # loads the dataset stored in the .csv file to a variable
    return pd.read_csv('docs/' + file + '.csv', low_memory=False, sep=";")

def split_date(name_year: str, name_month: str, name_day: str, column_name: str, df: pd.DataFrame) -> None:
    df[[name_year, name_month, name_day]] = [list(map(''.join, zip(*[iter(str(date))] * 2))) for date in df[column_name]]
    del df[column_name]


def read_account():
    df = pd.read_csv('./docs/account.csv', usecols=["account_id", "district_id",
        "frequency", "date"], sep=';')

    # Split Date into year, month and day
    split_date("creation_year", "creation_month", "creation_day", "date", df)

    df.to_csv('./preprocessing/account.csv', sep=';')


def read_loan_train():
    df = pd.read_csv('./docs/loan_train.csv', usecols=["loan_id", "account_id",
        "date", "amount", "duration", "payments", "status"], sep=';')

    # Split Date into year, month and day
    split_date("loan_year", "loan_month", "loan_day", "date", df)

    df.to_csv('./preprocessing/loan_train.csv', sep=';')

    df = pd.read_csv('./docs/loan_test.csv', usecols=["loan_id", "account_id",
        "date", "amount", "duration", "payments", "status"], sep=';')

    # Split Date into year, month and day
    split_date("loan_year", "loan_month", "loan_day", "date", df)

    df.to_csv('./preprocessing/loan_test.csv', sep=';')


def read_card_train():
    df = pd.read_csv("./docs/card_train.csv", sep=';')
    split_date("issued_year", "issued_month", "issued_day", "issued", df)
    df.to_csv("./preprocessing/card_train.csv", sep=";", index=False)


def read_district():
    df = pd.read_csv("./docs/district.csv", sep=';')

    # Region direction and Region
    df['region_direction'] = df['region'].apply(lambda x: x.split(" ")[0] if x.find(" ") != -1 else pd.NA)
    df['region'] = df['region'].apply(lambda x: x.split(" ")[1] if x.find(" ") != -1 else x)

    # Split name
    df['city_area'] = df['name'].apply(lambda x: x.split(" - ")[1] if x.find(" - ") != -1 else pd.NA)
    df['city'] = df['name'].apply(lambda x: x.split(" - ")[0] if x.find(" - ") != -1 else x)

    del df['name']
    del df['city_area']    # Not much information after analysis.

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
    df.to_csv("./preprocessing/district.csv", index=False, sep=";")

def parse_clients():
    # The client data is saved in the "client.csv" file
    dataframe = read_csv("client")

    # Separating the birth number into day, month and year
    dataframe.birth_number = dataframe.birth_number.astype('str')
    dataframe["birthdate_year"] = 1900 + dataframe.birth_number.str[:2].astype('int')
    dataframe["birthdate_month"] = dataframe.birth_number.str[2:4].astype('int')
    dataframe["birthdate_day"] = dataframe.birth_number.str[4:].astype('int')

    # The month was added by 50 for women, we are going to revert that and add a sex attribute
    dataframe["sex"] = np.where(dataframe.birthdate_month > 12, 'f', 'm')
    dataframe.loc[dataframe.sex == 'f', "birthdate_month"] = dataframe.birthdate_month - 50

    # Creating a birthdate column as a datetime
    dataframe["birthdate"] = (dataframe.birthdate_year.astype('str') + '-' +
                              dataframe.birthdate_month.astype('str') + '-' + dataframe.birthdate_day.astype('str'))
    dataframe.birthdate = pd.to_datetime(dataframe.birthdate)

    # Returning the dataframe without the now useless column birth_number
    return dataframe.drop(columns=["birth_number"])

if __name__ == "__main__":
    read_account()
    read_loan_train()
    read_card_train()
    read_district()
