from collections.abc import Callable

import numpy as np
import pandas as pd
import sqlite3

from numpy import NaN

from .sql import init_db
from .utils import read_csv, write_csv

def split_date_sql(date):
    year, month, day = list(map(''.join, zip(*[iter(str(date))] * 2)))
    year = str(int(year) + 1900)

    full_date = f"{year}-{month}-{day}"
    return year, month, day, full_date

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


def preprocess(file_name: str, parse_function):
    df = read_csv(file_name)
    df = parse_function(df)
    write_csv(df, file_name, index=False)

def process_account():
    connection = sqlite3.connect('./data/ac-v01.db')
    cursor = connection.cursor()

    cursor.execute("ALTER TABLE account ADD creation_date VARCHAR(255)")
    cursor.execute("ALTER TABLE account ADD creation_year INTEGER")
    cursor.execute("ALTER TABLE account ADD creation_month INTEGER")
    cursor.execute("ALTER TABLE account ADD creation_day INTEGER")
    connection.commit()

    cursor.execute("SELECT account_id, date FROM account")
    values = cursor.fetchall()
    for tup in values:
        c_id = tup[0]
        year, month, day, fulldate = split_date_sql(tup[1])
        cursor.execute(f"UPDATE account SET creation_date = {fulldate}, creation_year = {year}, creation_month = {month}, creation_day = {day} WHERE account_id = {c_id}")
    
    connection.commit()
    connection.close()

def process_card():
    connection = sqlite3.connect('./data/ac-v01.db')
    cursor = connection.cursor()

    cursor.execute("ALTER TABLE card ADD issued_date VARCHAR(255)")
    cursor.execute("ALTER TABLE card ADD issued_year INTEGER")
    cursor.execute("ALTER TABLE card ADD issued_month INTEGER")
    cursor.execute("ALTER TABLE card ADD issued_day INTEGER")
    connection.commit()

    cursor.execute("SELECT card_id, issued FROM card")
    values = cursor.fetchall()
    for tup in values:
        card_id = tup[0]
        year, month, day, fulldate = split_date_sql(tup[1])
        cursor.execute(f"UPDATE card SET issued_date = {fulldate}, issued_year = {year}, issued_month = {month}, issued_day = {day} WHERE card_id = {card_id}")
    
    connection.commit()
    connection.close()


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

def process_client():
    connection = sqlite3.connect('./data/ac-v01.db')
    cursor = connection.cursor()

    cursor.execute("ALTER TABLE client ADD birthdate VARCHAR(255)")
    cursor.execute("ALTER TABLE client ADD birthdate_year VARCHAR(255)")
    cursor.execute("ALTER TABLE client ADD birthdate_month VARCHAR(255)")
    cursor.execute("ALTER TABLE client ADD birthdate_day VARCHAR(255)")
    cursor.execute("ALTER TABLE client ADD sex VARCHAR(255)")
    connection.commit()

    cursor.execute("SELECT client_id, birthnumber FROM client")
    values = cursor.fetchall()

    for tup in values:
        client_id = tup[0]
        year = 1900 + int(str(tup[1])[:2])
        month = int(str(tup[1])[2:4])
        day = int(str(tup[1])[4:])
        if month > 12:
            month - 50
            genre = 'f' 
        else:
            genre = 'm'

        birthdate = f"{year}-{month}-{day}"
        cursor.execute(f"UPDATE client SET birthdate = '{birthdate}', birthdate_year = {year}, birthdate_month = {month}, birthdate_day = '{day}', sex = '{genre}'WHERE client_id = {client_id}")
    
    connection.commit()
    connection.close()


def process_disposition():
    connection = sqlite3.connect('./data/ac-v01.db')
    cursor = connection.cursor()

    cursor.execute("UPDATE disp SET type = LOWER(type)")
    connection.commit()
    connection.close()

def process_district():
    connection = sqlite3.connect('./data/ac-v01.db')
    cursor = connection.cursor()

    cursor.execute("ALTER TABLE district ADD region_direction VARCHAR(255)")
    connection.commit()

    cursor.execute("SELECT id, region, city FROM district")
    values = cursor.fetchall()
    for tup in values:
        district_id = tup[0]
        direction = tup[1].split(" ")[0] if tup[1].find(" ") != -1 else "NULL"
        region = tup[1].split(" ")[1] if tup[1].find(" ") != -1 else tup[1]
        name = tup[2].split(" - ")[0] if tup[2].find(" - ") != -1 else tup[2]
        
        cursor.execute(f"UPDATE district SET region_direction = '{direction}', region = '{region}', city = '{name}' WHERE id = {district_id}")
    
    connection.commit()
    connection.close()

def process_loan():
    connection = sqlite3.connect('./data/ac-v01.db')
    cursor = connection.cursor()

    cursor.execute("ALTER TABLE loan ADD loan_date VARCHAR(255)")
    cursor.execute("ALTER TABLE loan ADD loan_year INTEGER")
    cursor.execute("ALTER TABLE loan ADD loan_month INTEGER")
    cursor.execute("ALTER TABLE loan ADD loan_day INTEGER")
    connection.commit()

    cursor.execute("SELECT loan_id, date FROM loan")
    values = cursor.fetchall()
    for tup in values:
        loan_id = tup[0]
        year, month, day, fulldate = split_date_sql(tup[1])
        cursor.execute(f"UPDATE loan SET loan_date = {fulldate}, loan_year = {year}, loan_month = {month}, loan_day = {day} WHERE loan_id = {loan_id}")
    
    connection.commit()
    connection.close()

def process_transaction():
    connection = sqlite3.connect('./data/ac-v01.db')
    cursor = connection.cursor()

    cursor.execute("ALTER TABLE trans ADD trans_date VARCHAR(255)")
    cursor.execute("ALTER TABLE trans ADD trans_year INTEGER")
    cursor.execute("ALTER TABLE trans ADD trans_month INTEGER")
    cursor.execute("ALTER TABLE trans ADD trans_day INTEGER")
    connection.commit()

    cursor.execute("SELECT trans_id, date, operation FROM trans")
    values = cursor.fetchall()

    dict_map = {
        'credit in cash':'cash',
        'withdrawal in cash':'cash',
         'collection from another bank':'another bank',
         'remittance to another bank':'another bank',
        'credit card withdrawal':'credit card',
    }

    for tup in values:
        trans_id = tup[0]
        year, month, day, fulldate = split_date_sql(tup[1])
        operation = tup[2]
        if operation == '':
            operation = 'NULL'
        else:
            operation = dict_map[operation]
        cursor.execute(f"UPDATE trans SET operation = '{operation}', trans_date = {fulldate}, trans_year = {year}, trans_month = {month}, trans_day = {day} WHERE trans_id = {trans_id}")
    
    connection.commit()
    connection.close()

if __name__ == "__main__":
    init_db()
    
    process_account()
    process_card()
    process_client()
    process_disposition()
    process_district()
    process_loan()
    process_transaction()
