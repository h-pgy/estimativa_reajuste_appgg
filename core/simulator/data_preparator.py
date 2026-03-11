import pandas as pd
from core.utils.download_servidores import download_dados_servidores
from core.models.dados_originais_servidores import schema_dados_originais
from config import ENCODING_CSV_SERVIDORES

from typing import Optional

class Preparator:

    def __init__(self):

        self.download_dados_servidores = download_dados_servidores

    def load_df_original(self)->pd.DataFrame:

        fname = self.download_dados_servidores()
        df = pd.read_csv(fname, 
                         encoding=ENCODING_CSV_SERVIDORES, 
                         sep=';')
        
        return df

    def validate_df_original(self, df:pd.DataFrame)->pd.DataFrame:

        df = schema_dados_originais.validate(df)

        return df

    def load_df_original_pipeline(self)->pd.DataFrame:

        df = self.load_df_original()
        df = self.validate_df_original(df)

        return df

    def renomear_colunas(self, df:pd.DataFrame)->pd.DataFrame:

        df = df.copy(deep=True)

        renomear_cols = {
            'REGISTRO' : 'rf',
            'NOME' : 'nome',
            'REF_CARGO_BAS' : 'cargo_base',
            'SIGLA' : 'secretaria_dez_2025',
            'DATA_INICIO_EXERC' : 'dt_inicio_exercicio'
        }
        
        df.rename(renomear_cols, axis=1, inplace=True)

        return df


