# %%
import pandas as pd
from matplotlib import pyplot as plt
from pandas.core.frame import DataFrame
import numpy as np

dataPath = "../docs/card_train.csv"
df = pd.read_csv(dataPath, delimiter=";")


# %%
def preprocess_data() -> None:
    df['issued_year'] = df['issued'].apply(lambda x: x // 10000).astype(str)
    df['issued_year'].value_counts()

    df['issued_month'] = df['issued'].apply(
        lambda x: (x // 100) % 100).astype(str)
    df['issued_month'].value_counts()

    df['issued_day'] = df['issued'].apply(lambda x: x % 100).astype(str)
    df['issued_day'].value_counts()


def study_data() -> None:
    print("\n== Head:")
    print(df.head())

    print("\n== Tail:")
    print(df.tail())

    # There isn't null values.
    print("\n== Null data:")
    print(df.isnull().sum())

    # Possible values for fields.
    print("\n== Card type:")
    print(df.type.value_counts())


def show_bar_graph(x: pd.DataFrame, title: str) -> None:
    x_names = x.unique()
    x_freq = x.value_counts()

    plt.bar(x=x_names, height=x_freq)
    plt.title(title)
    plt.show()


# %%
study_data()
preprocess_data()
show_bar_graph(df['type'], 'Card type')
show_bar_graph(df['issued_year'], 'Issued year')
print(df)
