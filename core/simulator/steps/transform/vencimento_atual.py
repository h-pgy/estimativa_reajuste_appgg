from core.models.servidores import ServidorBaseDataframe
from core.models.tabelas import Tabela
import pandas as pd

class Vencimento:

    def __call__(self, df:pd.DataFrame, tabela:Tabela)->pd.DataFrame:


        tabela_dict = tabela.model_dump()
        df = ServidorBaseDataframe.validate(df)

        df['vencimento'] = df['nivel'].map(tabela_dict)

        return df

        