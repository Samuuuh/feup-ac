import pandas as pd
import os
class Builder:
    
    def read_frame(self, name: str) -> pd.DataFrame:
            position =  os.path.dirname(os.path.abspath(__file__)) + "/.."
            return pd.read_csv(position + '/data/preprocessed/' + name + '.csv', sep=';')