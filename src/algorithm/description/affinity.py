import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import AffinityPropagation
from sklearn.metrics import silhouette_score
import numpy as np


def affinity(df: pd.DataFrame) -> None:
    cluster_train = df[0].loc[:,["amount","min_balance","birthdate_year"]]

    # Declaring Model
    model = AffinityPropagation(max_iter=600, damping=0.95)

    model.fit(cluster_train) # Fitting Model
    all_predictions = model.predict(cluster_train) # Prediction on the entire data

    X = cluster_train

    # SCORE ===================================================================
    print(silhouette_score(X, all_predictions, metric='euclidean'))

    # PLOTING =================================================================
    fig = plt.figure(1, figsize=(8, 6))
    ax = Axes3D(fig, elev=-150, azim=110)
    ax.scatter(
        X.birthnumber,
        X.min_balance,
        X.amount,
        c=all_predictions,
        cmap=plt.cm.Set1,
        edgecolor="k",
        s=40,
    )

    ax.set_title("First three PCA directions")
    ax.set_xlabel("Birthnumber")
    ax.w_xaxis.set_ticklabels([])
    ax.set_ylabel("Min Balance")
    ax.w_yaxis.set_ticklabels([])
    ax.set_zlabel("Mean Balance")
    ax.w_zaxis.set_ticklabels([])

    plt.show()
