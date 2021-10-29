# import libraries
import numpy as np
import pandas as pd


def read_csv(file):
    # loads the dataset stored in the .csv file to a variable
    return pd.read_csv('docs/' + file + '.csv', low_memory=False, sep=";")


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


# main function
if __name__ == "__main__":
    clients = parse_clients()
    print(clients)
