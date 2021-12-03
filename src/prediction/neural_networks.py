from sklearn.neural_network import MLPClassifier  
import pandas as pd 
from .utils import get_x, get_y, save_result 
from sklearn.model_selection import train_test_split 
from imblearn.over_sampling import SMOTE 
from sklearn.metrics import roc_auc_score 

def neural_network_smote(df_dev: pd.DataFrame, df_comp: pd.DataFrame, debug: bool) -> None:   

    x = get_x(df_dev)
    y = get_y(df_dev) 

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, stratify=y) 
    smp = SMOTE()
    x_res, y_res = smp.fit_resample(x_train, y_train) 

    clf = MLPClassifier(hidden_layer_sizes=(15,), random_state=1, max_iter=1, warm_start=True)  
    clf.fit(x_res, y_res)  

    predicted = clf.predict_proba(x_test)[::, 1]
    expected = y_test 
    print(f"score {roc_auc_score(expected, predicted)}") 

    if not debug: 
        pred_competition = clf.predict_proba(get_x(df_comp))
        save_result(df_comp['loan_id'], pred_competition[::, 1], 'neural_network')