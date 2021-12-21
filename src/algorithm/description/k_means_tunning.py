import pandas as pd
from sklearn import cluster
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from kneed import KneeLocator


def k_means_tunning(df: pd.DataFrame) -> None:
    cluster_train = df[0].loc[:, ["amount", "min_balance", "birthdate_year"]]

    # BEST NUMBER OF CLUSTERINGS (ELBOW) ======================================
    kmeans_kwargs = {
        "init": "random",
        "n_init": 10,
        "max_iter": 300,
        "random_state": 42,
    }

    # A list holds the SSE values for each k
    sse = []
    for k in range(1, 11):
        kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
        kmeans.fit(cluster_train)
        sse.append(kmeans.inertia_)

    # Visualize what is the best number of clusterings.
    plt.style.use("fivethirtyeight")
    plt.plot(range(1, 11), sse)
    plt.xticks(range(1, 11))
    plt.xlabel("Number of Clusters")
    plt.ylabel("SSE")
    plt.show()

    # Getting the best number of clusters.
    kl = KneeLocator(range(1, 11), sse, curve="convex", direction="decreasing")
    clusters_number = kl.elbow

    # TRAIN ===================================================================
    kmeans = KMeans(n_clusters=clusters_number, **kmeans_kwargs)
    kmeans.fit(cluster_train)
    all_predictions = kmeans.predict(cluster_train)

    X = cluster_train

    # SCORE ===================================================================
    labels = kmeans.labels_
    print(silhouette_score(X, labels, metric='euclidean'))

    # PLOTING =================================================================
    fig = plt.figure(1, figsize=(8, 6))
    ax = Axes3D(fig, elev=-150, azim=110)
    ax.scatter(
        X.birthdate_year,
        X.min_balance,
        X.amount,
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

    """
    fig = plt.figure(1, figsize=(8, 6))
    ax = plt.gca()
    ax.scatter(
        X.amount,
        X.min_balance,
        c=all_predictions,
        cmap=plt.cm.Set1,
        edgecolor="k",
        s=40,
    )
    #ax.set_title("First three PCA directions")
    #ax.set_xlabel("1st eigenvector")
    #ax.w_xaxis.set_ticklabels([])
    #ax.set_ylabel("2nd eigenvector")
    #ax.w_yaxis.set_ticklabels([])

    plt.show()
    """
