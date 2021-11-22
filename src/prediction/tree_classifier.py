import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score

from .utils import get_x, get_y, save_result

def tree_classifier(df_dev: pd.DataFrame, df_comp: pd.DataFrame, debug: bool) -> None:

    # Divide development data into test and train
    train, test = train_test_split(df_dev, test_size=0.2)

    # Train the model
    x = get_x(train)
    y = get_y(train)

    log_reg = DecisionTreeClassifier(max_depth=4)
    log_reg.fit(x, y)


    # Apply training
    if debug:
        predicted = log_reg.predict_proba(get_x(test))[::, 1]
        expected  = get_y(test)
        print(f"score {roc_auc_score(expected, predicted)}")
    else: 
        pred_competition = log_reg.predict_proba(get_x(df_comp))   
        save_result(df_comp['loan_id'], pred_competition[::, -1], 'grid_log_reg')


