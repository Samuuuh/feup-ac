from sklearn.ensemble import RandomForestClassifier
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from imblearn.over_sampling import SMOTE

from .utils import get_x, get_y, save_result
from sklearn.feature_selection import SelectKBest


def random_forest_smote_kbest(df_dev: pd.DataFrame, df_comp: pd.DataFrame, debug: bool) -> None:
    #X, y = load_digits(return_X_y=True)
    #X.shape
    #X_new = SelectKBest(chi2, k=20).fit_transform(X, y)
    #X_new.shape

    x = get_x(df_dev)
    y = get_y(df_dev) 

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, stratify=y)

    smp = SMOTE()
    x_res, y_res = smp.fit_resample(x_train, y_train)
    clf = RandomForestClassifier(n_estimators=100, max_depth=30, class_weight="balanced")
    clf.fit(x_res, y_res)

    
    predicted = clf.predict_proba(x_test)[::, 1]
    expected = y_test
    print(f"score {roc_auc_score(expected, predicted)}") 
    
    if not debug: 
        pred_competition = clf.predict_proba(get_x(df_comp))
        save_result(df_comp['loan_id'], pred_competition[::, 1], 'random_forest')