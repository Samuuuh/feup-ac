import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score

def agglomerative_clustering(df: pd.DataFrame) -> None:
    df = df[0].loc[:,["amount","min_balance","birthdate_year"]]

    clustering = AgglomerativeClustering().fit(df)
    all_predictions = clustering.labels_

    X = df

    # SCORE ===================================================================
    print(silhouette_score(X, all_predictions, metric='euclidean'))

    # PLOTING =================================================================
    fig = plt.figure(1, figsize=(8, 6))
    ax = Axes3D(fig, elev=-150, azim=110)
    ax.scatter(
        X.amount,
        X.min_balance,
        X.birthnumber,
        c=all_predictions,
        cmap=plt.cm.Set1,
        edgecolor="k",
        s=40,
    )
    ax.set_title("First three PCA directions")
    ax.set_xlabel("Amount")
    ax.w_xaxis.set_ticklabels([])
    ax.set_ylabel("Min Balance")
    ax.w_yaxis.set_ticklabels([])
    ax.set_zlabel("Birthnumber")
    ax.w_zaxis.set_ticklabels([])

    plt.show()

