import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import KFold
from .model import Model
import numpy as np


class RegressionGrid(Model):
    def __init__(self, argument_columns: list[str], goal_column: str) -> None:
        super().__init__()
        self.log_reg = None
        self.argument_columns = argument_columns
        self.goal_column = goal_column
        self.init()

    def init(self) -> None:

        """Init the GridSearchCV and LogiticRegression variables.

        Sources:
            KFold: https://scikit-learn.org/stable/modules/cross_validation.html
            param_grid: https://towardsdatascience.com/grid-search-for-model-tuning-3319b259367e
            scoring possibilities: https://towardsdatascience.com/grid-search-for-model-tuning-3319b259367e
        """


        self.log_reg = LogisticRegression()
        cv = KFold()                                

        param_grid = {
            'penalty': ['l2'],                        
            'C': np.logspace(-3,3,7)    # Inverse of regularization.
        }

        self.grid = GridSearchCV(
                        estimator = self.log_reg,
                        param_grid = param_grid,        
                        scoring = 'roc_auc',            
                        cv = cv) 


    def train(self, dataframe: pd.DataFrame) -> None:
        # Get the data
        x = dataframe.loc[:, self.argument_columns]
        y = dataframe.status

        # Apply the regression
        self.grid.fit(x, y)


    def test(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        arguments = dataframe.loc[:, self.argument_columns]
        prediction = self.grid.predict_proba(arguments)[:, 0]
        return pd.DataFrame({'Id': dataframe.loan_id, 'Predicted': prediction}).set_index('Id')



        