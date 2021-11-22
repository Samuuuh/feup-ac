import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

from .utils import get_x, get_y

def log_regression(df_dev: pd.DataFrame, df_comp: pd.DataFrame, debug: bool) -> None:

    # Divide development data into test and train
    train, test = train_test_split(df_dev, test_size=0.2)

    # Train the model
    x = get_x(train)
    y = get_y(train)

    # Apply the regression
    log_reg = LogisticRegression()
    log_reg.fit(x, y)

    # Test
    predicted = log_reg.predict(get_x(test))
    expected  = get_y(test)
    print(f"score {roc_auc_score(expected, predicted)}")



    




