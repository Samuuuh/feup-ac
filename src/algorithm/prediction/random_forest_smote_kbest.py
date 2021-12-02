from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from imblearn.over_sampling import SMOTE
from .utils import get_x, get_y, print_feature_importance, save_result, save_model, read_model
from sklearn.feature_selection import SelectKBest, f_classif

# Robust against outliers. 
# Highly correlated variables may distort te random forest. 
def random_forest_smote_kbest(df_dev: pd.DataFrame, df_comp: pd.DataFrame, debug: bool) -> None: 
    n_estimators  = [100, 300, 500, 800, 1200]
    max_depth = [5, 8, 15, 30]
    min_samples_split = [2, 5, 10, 15, 100]
    min_samples_leaf = [1,2,5,10]
    hyperF = dict(n_estimators = n_estimators, max_depth = max_depth,
    min_samples_split = min_samples_split, min_samples_leaf = min_samples_leaf)

    x = get_x(df_dev)
    y = get_y(df_dev)  
    k_best = SelectKBest(f_classif, k=11)

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, stratify=y)

    smp = SMOTE()
    x_res, y_res = smp.fit_resample(x_train, y_train)
    x_res = k_best.fit_transform(x_res, y_res)

    # Uncoment to train again. 
    #clf = RandomForestClassifier()
    #clf = GridSearchCV(clf, hyperF, cv = 3, verbose = 1, n_jobs = -1)
    #clf.fit(x_res, y_res)
    #save_model(clf, "random_forest_kbest_grid_smote")  
    
    clf: GridSearchCV = read_model("random_forest_kbest_grid_smote")  


    # Selecting columns
    cols = k_best.get_support() 

    x_test = x_test.iloc[:, cols]
    predicted = clf.predict_proba(x_test)[::, 1]
    expected = y_test 

    print(f"score {roc_auc_score(expected.values, predicted)}") 
    print_feature_importance(clf.best_estimator_.feature_importances_, x_train.columns[(cols)])

    if not debug: 
        x_comp = get_x(df_comp).iloc[:, cols]
        pred_competition = clf.predict_proba(x_comp)
        save_result(df_comp['loan_id'], pred_competition[::, 1], 'random_forest_kbest')


