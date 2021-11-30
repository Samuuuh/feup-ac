#!/bin/python3

# Libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def read_frame(name: str) -> pd.DataFrame:
    return pd.read_csv('../data/preprocessed/' + name + '.csv', sep=';')


loans = read_frame('loan_dev')
accounts = read_frame('account')
districts = read_frame('district')

x = 3

####################################################################################################
# Barplot - 3D
####################################################################################################

if x == 0:
       loan_accounts = pd.merge(loans, accounts, how="left", on=["account_id"])
       loan_districts = pd.merge(loan_accounts, districts,
                            how="left", on=["district_id"])

       group = loan_districts.groupby(['region'])
       group_default = loan_districts.loc[loan_districts.status == -1].groupby(['region'])
       group_non_default = loan_districts.loc[loan_districts.status == 1].groupby(['region'])

       regions = group.region.indices.keys()
       number_of_loans = group.count().status.values
       defaulted_loans = group_default.count().status.values
       non_defaulted_loans = group_non_default.count().status.values
       width = 0.35

       fig, ax = plt.subplots()

       ax.bar(regions, non_defaulted_loans, width, label='Non-Defaulted')
       ax.bar(regions, defaulted_loans, width, label='Defaulted')

       ax.set_ylabel('Number of Loans')
       ax.set_title('Status of Regions')
       ax.legend()
       plt.show()

####################################################################################################
# Piechart - 2D
####################################################################################################

elif x == 1:
       group = loans.groupby(['status'])
       count = group.count()

       fig, ax = plt.subplots()
       ax.pie(count.loan_id.values, radius=2, center=(4, 4),
              wedgeprops={"linewidth": 1, "edgecolor": "white"}, labels=["Defaulted", ""])

       ax.set(xlim=(0, 8),
              ylim=(0, 8))

       plt.show()

####################################################################################################
# Line Plots - 2D
####################################################################################################

elif x == 2:
       group = loans.groupby(["loan_year", "loan_month"])
       group_months = group.count().loan_id

       x = group.indices.keys()
       x = [year + (month - 1) / 12 for year, month in x]
       y = group_months.values

       fig, ax = plt.subplots()
       ax.plot(x, y, linewidth=2.0)

       ax.set(xlim=(1993, 1997), xticks=np.arange(1993, 1998),
              ylim=(0, 15))

       ax.set_ylabel('Number of Loans')
       ax.set_title('Number of Loans by Month')

       plt.show()

####################################################################################################
# Scatterplot - 4D
####################################################################################################

elif x == 3:
       districts = districts.loc[districts.perc_unemploy_95 != "?"]

       districts["perc_unemploy_95"] = pd.to_numeric(districts.perc_unemploy_95)
       districts['perc_unemploy'] = (districts.perc_unemploy_95 + districts.perc_unemploy_96) / 2
       conditions = [
              districts.region == 'Moravia',
              districts.region == 'Bohemia',
              districts.region == 'Prague'
       ]
       choices = ['blue', 'red', 'yellow']
       districts['colour'] = np.select(conditions, choices, default='black')

       inhabitants = districts.num_inhab / 3000
       salary = districts.avg_salary
       perc_unemploy = districts.perc_unemploy
       colors = districts.colour

       x = salary.values
       y = perc_unemploy.values
       area = inhabitants.values

       fig, ax = plt.subplots()
       scatter = ax.scatter(x, y, s=area, c=colors, alpha=0.5)

       """
       legend1 = ax.legend(*scatter.legend_elements(),
                    loc="lower left", title="Regions")
       ax.add_artist(legend1)
       handles, labels = scatter.legend_elements(prop="sizes", alpha=0.6)
       legend2 = ax.legend(handles, labels, loc="upper right", title="Sizes")
       """

       plt.show()