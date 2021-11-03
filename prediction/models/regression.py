import pandas as pd
from sklearn.linear_model import LogisticRegression

from .model import Model


class Regression(Model):
    def __init__(self, argument_columns: list[str], goal_column: str) -> None:
        super().__init__()
        self.log_reg = None
        self.argument_columns = argument_columns
        self.goal_column = goal_column

    def train(self, dataframe: pd.DataFrame) -> None:
        # Get the data
        x = dataframe.loc[:, self.argument_columns]
        y = dataframe.status

        # Apply the regression
        self.log_reg = LogisticRegression()
        self.log_reg.fit(x, y)

    def test(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        arguments = dataframe.loc[:, self.argument_columns]
        prediction = self.log_reg.predict_proba(arguments)[:, 0]
        return pd.DataFrame({'Id': dataframe.loan_id, 'Predicted': prediction}).set_index('Id')

    def score(self) -> float:
        return 0