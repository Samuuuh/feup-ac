import pandas as pd
import time

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
import matplotlib.pyplot as plt

from .utils import get_x, get_y, save_result

def log_regression(df_dev: pd.DataFrame, df_comp: pd.DataFrame, debug: bool) -> None:
    start = time.time()

    # Divide development data into test and train
    train, test = train_test_split(df_dev, test_size=0.2)

    # Train the model
    x = get_x(train)
    y = get_y(train)

    log_reg = LogisticRegression(max_iter=2500)
    log_reg.fit(x, y)

    xy = list(zip(log_reg.feature_names_in_, log_reg.coef_[0]))
    xy = filter(lambda x: abs(x[1]) > 0.0001, xy)
    xy = sorted(xy, key=lambda x: -x[1])
    # xy = filter(lambda x: abs(x[1]) > 0.01, xy)
    x = [e[0] for e in xy]
    y = [e[1] for e in xy]

    plt.barh(x, y, edgecolor="white", linewidth=0.7)
    plt.show()

    end = time.time()
    print(f"Time elapsed: {end - start}")
    # Apply training
    if debug:
        predicted = log_reg.predict_proba(get_x(test))[::, 1]
        expected  = get_y(test)
        print(f"score {roc_auc_score(expected, predicted)}")
    else:
        pred_competition = log_reg.predict_proba(get_x(df_comp))
        save_result(df_comp['loan_id'], pred_competition[::, 1], 'grid_log_reg')
