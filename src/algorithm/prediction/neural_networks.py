from sklearn.neural_network import MLPClassifier  
import pandas as pd 
from .utils import get_x, get_y, save_result 
from sklearn.model_selection import train_test_split 
from imblearn.over_sampling import SMOTE 
from sklearn.metrics import roc_auc_score 
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV

def transform(arr):  
    for i in range(len(arr)):  
        if arr[i] < 0.001:
            arr[i] = 0

    return arr

# Perceptron is sensitive to feature scaling, so we scaled our data. 
def neural_network_smote(df_dev: pd.DataFrame, df_comp: pd.DataFrame, debug: bool) -> None:   

    x = get_x(df_dev)
    y = get_y(df_dev)  
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, stratify=y)  

    hyper_f = dict(hidden_layer_sizes= [100, 200, 300], activation= ['identity', 'logistic', 'tanh', 'relu'], 
    solver= ["lbfgs"], learning_rate= ["constant", "adaptative"], max_iter= [200,300,400])

    scaler = StandardScaler()
    scaler.fit(x_train)
    x_train = scaler.transform(x_train)
    x_test = scaler.transform(x_test)


    clf = MLPClassifier()  
    clf = GridSearchCV(clf, hyper_f , cv=3, n_jobs=-1)
    clf.fit(x_train, y_train)  

    predicted = transform(clf.predict_proba(x_test)[::, 1])
    expected = y_test

    cols = 
    print(f"score {roc_auc_score(expected, predicted)}")
    print_feature_importance(clf.best_estimator_.feature_importances_, x_train.columns[(cols)])
    if not debug: 
        x_comp = scaler.transform(get_x(df_comp))
        pred_competition = clf.predict_proba(x_comp)
        save_result(df_comp['loan_id'], transform(pred_competition[::, 1]), 'neural_network') 
