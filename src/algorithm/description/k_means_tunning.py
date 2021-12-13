import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def k_means_tunning(df: pd.DataFrame) -> None:
    cluster_train = df[0].loc[:,["amount","min_balance","payments"]]

    # Declaring Model
    model = KMeans(n_clusters=4)

    #X = cluster_train.loc[:,["only_na_account","min_balance"]]
    # only_na_account
    # min_balance

    model.fit(cluster_train) # Fitting Model
    all_predictions = model.predict(cluster_train) # Prediction on the entire data

    X = cluster_train

    fig = plt.figure(1, figsize=(8, 6))
    ax = Axes3D(fig, elev=-150, azim=110)
    ax.scatter(
        X.amount,
        X.min_balance,
        X.payments,
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
    ax.set_zlabel("Type Sanction")
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