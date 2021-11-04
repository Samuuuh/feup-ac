import pandas as pd
from sklearn.model_selection import train_test_split

from prediction.models.model import Model
from prediction.models.regression import Regression


def read_frame(name: str):
    return pd.read_csv('./data/preprocessed/' + name + '.csv', sep=';')


def simple():
    development = read_frame("loan_dev")

    # Divide development data into test and train
    train, test = train_test_split(development, test_size=0.2)

    # Train the model
    regression = Regression(['amount', 'loan_year', 'payments', 'duration'], 'status')
    regression.train(train)

    # Test the model
    prediction = regression.test(train)
    expected = Model.get_expected(train, "loan_id", "status")
    print("Score: ", regression.score(expected, prediction))
    regression.plot_roc()

    # Apply to competition data
    # competition = read_frame("loan_comp")
    # prediction = regression.test(competition)
    # prediction.to_csv('./data/submission/sub-linear.csv')


if __name__ == "__main__":
    simple()
