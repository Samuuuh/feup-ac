from matplotlib import pyplot as plt
import pandas as pd


def search_nulls(df: pd.DataFrame) -> None:
    print("\n== Null data:")
    print(df.isnull().sum())


def show_head_tail(df: pd.DataFrame) -> None:
    print("\n== Head:")
    print(df.head())

    print("\n== Tail:")
    print(df.tail())


def study_district():
    df = pd.read_csv("./preprocessing/district.csv", sep=";")

    show_head_tail(df)
    search_nulls(df)

    # Possible regions
    print("\n== Regions:")
    print(df['region'].value_counts())

    # How to fillna in region directions
    df_filter = df['region'] == 'Bohemia'      # the null value is in the bohemia region.
    print(df.where(df_filter)['region_direction'].value_counts())
    df['region_direction'] = df['region_direction'].fillna("central")



def study_card():
    df = pd.read_csv("./docs/card_train.csv", sep=";")

    show_head_tail(df)
    search_nulls(df)

    # Possible values for fields.
    print("\n== Card type:")
    print(df.type.value_counts())


if __name__ == '__main__':
    study_district()
