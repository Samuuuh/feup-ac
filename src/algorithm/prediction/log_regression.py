import pandas as pd
import time

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

from .utils import get_x, get_y, save_result

def log_regression(df_dev: pd.DataFrame, df_comp: pd.DataFrame, debug: bool) -> None:
    start = time.time()

    # Divide development data into test and train
    train, test = train_test_split(df_dev, test_size=0.2)

    # Train the model
    x = get_x(train)
    y = get_y(train)

    log_reg = LogisticRegression()
    log_reg.fit(x, y)

    print(f"Time elapsed: {end - start}")
    # Apply training
    if debug:
        predicted = log_reg.predict_proba(get_x(test))[::, 1]
        expected  = get_y(test)
        print(f"score {roc_auc_score(expected, predicted)}")
    else:
        pred_competition = log_reg.predict_proba(get_x(df_comp))
        save_result(df_comp['loan_id'], pred_competition[::, 1], 'grid_log_reg')
