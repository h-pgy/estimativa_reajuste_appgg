import pandas as pd
from core.utils.download_servidores import download_dados_servidores
from core.models.dados_originais_servidores import schema_dados_originais
from typing import Optional
from config import ENCODING_CSV_SERVIDORES

class Loader:

    def __init__(self)->None:

        self.load_original_data = download_dados_servidores

    def load_df_original(self)->pd.DataFrame:

        fname = self.load_original_data()
        df = pd.read_csv(fname, 
                         encoding=ENCODING_CSV_SERVIDORES, 
                         sep=';')
        
        return df

    def validate_df_original(self, df:pd.DataFrame)->pd.DataFrame:

        df = schema_dados_originais.validate(df)

        return df
    
    def __call__(self, df:Optional[pd.DataFrame]=None)->pd.DataFrame:

        self.df = df or self.load_df_original()
        df = self.validate_df_original(self.df)

        return df