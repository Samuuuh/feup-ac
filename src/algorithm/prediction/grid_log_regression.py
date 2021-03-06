import pandas as pd
import numpy as np
import time

from sklearn.model_selection import train_test_split, KFold, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score

from .utils import get_x, get_y, save_result


def grid_log_regression(df_dev: pd.DataFrame, df_comp: pd.DataFrame, debug: bool) -> None:
    start = time.time()

    # Divide development data into test and train
    train, test = train_test_split(df_dev, test_size=0.2)

    # Train the model
    x = get_x(train)
    y = get_y(train)

    # Other types of validation. three-fold-validation, for example.
    log_reg = LogisticRegression(max_iter=2500)
    cross_validation = KFold()
    parameter_grid={"C": np.logspace(-3,-3, 7), "penalty": ["l2"]}
    grid_search = GridSearchCV(
        log_reg,
        param_grid = parameter_grid,
        cv = cross_validation,
        scoring='roc_auc'
    )
    grid_search.fit(x, y.values.ravel())

    # Apply training
    predicted = grid_search.predict_proba(get_x(test))[::, 1]
    expected  = get_y(test)
    print(f"score {roc_auc_score(expected, predicted)}")
    end = time.time()
    print(f"Time elapsed: {end - start}")

    if not debug:
        pred_competition = grid_search.predict_proba(get_x(df_comp))
        save_result(df_comp['loan_id'], pred_competition[::, 1], 'grid_log_reg')
