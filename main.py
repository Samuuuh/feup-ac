import pandas as pd

from sklearn.datasets import make_blobs
from sklearn.linear_model import LogisticRegression

def simple():
    train = pd.read_csv('./preprocessing/loan_train.csv', usecols=['loan_id', 'account_id', 'loan_year', 'loan_month', 'loan_day',  'amount', 'duration', 'payments', 'status'], sep=';')
    feature_cols = ['amount', 'loan_year', 'payments', 'duration']
    X = train.loc[:, feature_cols]
    y = train.status

    logreg = LogisticRegression()
    logreg.fit(X, y)

    test = pd.read_csv('./preprocessing/loan_test.csv', usecols=['loan_id', 'account_id', 'loan_year', 'loan_month', 'loan_day', 'amount', 'duration', 'payments'], sep=';')
    X_new = test.loc[:, feature_cols]
    new_pred_class = logreg.predict(X_new)

    kaggle_data = pd.DataFrame({'Id':test.loan_id, 'Predicted':logreg.predict_proba(X_new)[:,0]}).set_index('Id')
    kaggle_data.to_csv('./submission/sub-linear.csv')

if __name__ == "__main__":
    simple()