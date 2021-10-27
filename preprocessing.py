import pandas as pd

def read_account():
    df = pd.read_csv('./docs/account.csv', usecols=["account_id", "district_id", "frequency", "date"], sep=';')
    
    # Split Date into year, month and day
    df[["year", "month", "day"]] = [list(map(''.join, zip(*[iter(str(date))]*2))) for date in df["date"]]
    del df["date"]

    df.to_csv('./preprocessing/account.csv', sep=';')

if __name__ == "__main__":
    read_account()