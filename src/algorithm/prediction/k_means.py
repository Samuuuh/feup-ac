import pandas as pd
import time

from imblearn.over_sampling import SMOTE
from sklearn.cluster import KMeans
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from .utils import get_x, get_y, save_result


def k_means(df_dev: pd.DataFrame, df_comp: pd.DataFrame, debug: bool):
    start = time.time()

    df_dev.sort_values(['loan_date'])
    df_dev = df_dev.drop(columns=['loan_date'])
    df_comp = df_comp.drop(columns=['loan_date'])
    print(df_comp.columns)

    # Train and test split
    x = get_x(df_dev)
    y = get_y(df_dev)
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, stratify=None, shuffle=False)

    # Sampling
    smp = SMOTE()
    x_res, y_res = smp.fit_resample(x_train, y_train)

    # Standardization
    scaler = StandardScaler()
    scaled_x = scaler.fit_transform(x)

    for _ in range(1):
        # Run the K-Means algorithm
        kmeans = KMeans(
            n_clusters=2,
            max_iter=300,
        )

        estimator = kmeans.fit(scaled_x)

        predicted = estimator.predict(x_test.values)
        expected = y_test
        score = roc_auc_score(expected, predicted)

        print(predicted)

        print(f"score {score}")
        print(f"Time elapsed: {end - start}")

    if not debug:
        pred_competition = estimator.predict(get_x(df_comp))
        save_result(df_comp['loan_id'], pred_competition, 'k_means')
