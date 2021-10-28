from matplotlib import pyplot as plt
import pandas as pd


def study_card():
    df = pd.read_csv("./docs/card_train.csv", sep=";")

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


if __name__ == '__main__':
    study_card()
