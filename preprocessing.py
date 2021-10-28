import pandas as pd

def split_date(name_year, name_month, name_day, df):
    df[[name_year, name_month, name_day]] = [list(map(''.join, zip(*[iter(str(date))]*2))) for date in df["date"]]
    del df["date"]

def read_account():
    df = pd.read_csv('./docs/account.csv', usecols=["account_id", "district_id", \
        "frequency", "date"], sep=';')
    
    # Split Date into year, month and day
    split_date("creation_year", "creation_month", "creation_day", df)

    df.to_csv('./preprocessing/account.csv', sep=';')

def read_loan_train():
    df = pd.read_csv('./docs/loan_train.csv', usecols=["loan_id", "account_id", \
        "date", "amount", "duration", "payments", "status"], sep=';')
    
    # Split Date into year, month and day
    split_date("loan_year", "loan_month", "loan_day", df)

    df.to_csv('./preprocessing/loan_train.csv', sep=';')

if __name__ == "__main__":
    read_account()
    read_loan_train()