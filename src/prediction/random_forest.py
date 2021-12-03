from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from imblearn.over_sampling import SMOTE

from .utils import get_x, get_y, save_result

def random_forest(df_dev: pd.DataFrame, df_comp: pd.DataFrame, debug: bool) -> None:

    x = get_x(df_dev)
    y = get_y(df_dev) 

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, stratify=y)

    clf = RandomForestClassifier(n_estimators=100, max_depth=30)
    clf.fit(x_train, y_train)

    if debug:
        predicted = clf.predict_proba(x_test)[::, 0]
        expected = y_test
        print(f"score {roc_auc_score(expected, predicted)}")
    else: 
        pred_competition = clf.predict_proba(get_x(df_comp))
        save_result(df_comp['loan_id'], pred_competition[::, 0], 'random_forest')