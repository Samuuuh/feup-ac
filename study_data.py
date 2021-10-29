# %% 
from os import defpath
from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns


df_loan = pd.read_csv("./preprocessing/loan_train.csv", sep=";")
df_dist = pd.read_csv("./preprocessing/district.csv", sep=";")
df_card = pd.read_csv("./preprocessing/card_train.csv", sep=";")
df_acct = pd.read_csv("./preprocessing/account.csv", sep=";")


def search_nulls(df: pd.DataFrame) -> None:
    print("\n== Null data:")
    print(df.isnull().sum())


def show_head_tail(df: pd.DataFrame) -> None:
    print("\n== Head:")
    print(df.head())

    print("\n== Tail:")
    print(df.tail())


def show_corr_matrix(corr):
    ax = sns.heatmap(
        corr,
        vmin=-1, vmax=1, center=0,
        cmap=sns.diverging_palette(20, 220, n=200),
        square=True,
    )
    ax.set_xticklabels(
        ax.get_xticklabels(),
        rotation=45,
        horizontalalignment='right'
    )


def study_district():

    show_head_tail(df_dist)
    search_nulls(df_dist)

    # Possible regions
    print("\n== Regions:")
    print(df_dist['region'].value_counts())

    # How to fillna in region directions
    df_filter = df_dist['region'] == 'Bohemia'      # the null value is in the bohemia region.
    print(df_dist.where(df_filter)['region_direction'].value_counts())


def study_card():

    show_head_tail(df_card)
    search_nulls(df_card)

    # Possible values for fields.
    print("\n== Card type:")
    print(df_card.type.value_counts())


# %%
def corrlation_with_status():

    print("== CORRELATION WITH STATUS (LOAN AND CARD)")
    df_loan_card = df_loan.join(df_card, how='inner')
    print(df_loan_card.corrwith(df_loan_card['status']))
    show_corr_matrix(df_loan_card.corr())
    # print(df_loan_card.corr())

    print("\n== CORRELATION WITH STATUS (LOAN AND CARD)")
    df_loan_acct = df_loan.join(df_acct, how='inner', on='account_id', rsuffix='acct')
    print(df_loan_acct.corrwith(df_loan_acct['status']))
    show_corr_matrix(df_loan_acct.corr())


if __name__ == '__main__':
    corrlation_with_status()


# %%
