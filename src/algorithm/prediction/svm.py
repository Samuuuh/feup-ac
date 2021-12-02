from sklearn.svm import SVC
from sklearn.pipeline import make_pipeline
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score 
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from .utils import get_x, get_y, print_feature_importance, save_result
from sklearn.feature_selection import SelectKBest, f_classif


def svm_model(df_dev: pd.DataFrame, df_comp: pd.DataFrame, debug: bool) -> None:
    x = get_x(df_dev)
    y = get_y(df_dev)  
    k_best = SelectKBest(f_classif, k=7)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, stratify=y)

    smp = SMOTE()
    x_res, y_res = smp.fit_resample(x_train, y_train)
    x_res = k_best.fit_transform(x_res, y_res)

    scaler = StandardScaler()
    scaler.fit(x_res)
    x_res = scaler.transform(x_res)
    x_res = scaler.transform(x_res)

    clf = SVC(gamma='auto', probability=True, kernel="linear")
    clf.fit(x_res, y_res)

    # Selecting columns
    cols = k_best.get_support() 

    x_test = x_test.iloc[:, cols]
    predicted = clf.predict_proba(x_test)[::, 1]
    expected = y_test 

    print(f"score {roc_auc_score(expected.values, predicted)}") 
    if not debug: 
        x_comp = get_x(df_comp).iloc[:, cols]
        pred_competition = clf.predict_proba(x_comp)
        save_result(df_comp['loan_id'], pred_competition[::, 1], 'random_forest_kbest')



