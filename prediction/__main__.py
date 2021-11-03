import pandas as pd

from prediction.models.regression import Regression


def read_frame(name: str):
    return pd.read_csv('./data/preprocessed/' + name + '.csv', sep=';')


def simple():
    train = read_frame("loan_dev")
    test = read_frame("loan_comp")

    regression = Regression(['amount', 'loan_year', 'payments', 'duration'], 'status')
    regression.train(train)
    prediction = regression.test(test)

    prediction.to_csv('./data/submission/sub-linear.csv')


if __name__ == "__main__":
    simple()
