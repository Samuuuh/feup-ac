import pandas as pd
from sklearn.linear_model import LogisticRegression


def read_frame(name: str):
    return pd.read_csv('./preprocessing/' + name + '.csv', sep=';')


def simple():
    train = read_frame("loan_train")
    feature_cols = ['amount', 'loan_year', 'payments', 'duration']
    x = train.loc[:, feature_cols]
    y = train.status

    log_reg = LogisticRegression()
    log_reg.fit(x, y)

    test = read_frame("loan_test")
    x_new = test.loc[:, feature_cols]
    new_pred_class = log_reg.predict(x_new)

    kaggle_data = pd.DataFrame({'Id': test.loan_id, 'Predicted': log_reg.predict_proba(x_new)[:, 0]}).set_index('Id')
    kaggle_data.to_csv('./submission/sub-linear.csv')


if __name__ == "__main__":
    simple()
