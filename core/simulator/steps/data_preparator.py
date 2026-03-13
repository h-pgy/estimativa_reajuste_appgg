import pandas as pd
from .data_loader import Loader
from core.models.servidores import ServidorBaseDataframe
from typing import Optional

class Preparator:

    def __init__(self)->None:

        self.load_original_data = Loader()

    def renomear_colunas(self, df:pd.DataFrame)->pd.DataFrame:

        renomear_cols = {
            'REGISTRO' : 'rf',
            'NOME' : 'nome',
            'REF_CARGO_BAS' : 'cargo_base',
            'SIGLA' : 'secretaria_dez_2025',
            'DATA_INICIO_EXERC' : 'dt_inicio_exercicio'
        }
        
        df = df.rename(renomear_cols, axis=1)

        return df
    

    def obter_nivel_carreira(self, df:pd.DataFrame)->pd.DataFrame:

        df['nivel_carreira'] = df['cargo_base'].str.extract(r'(\d+)$').astype(int)

        return df
    
    def dt_inicio_exercicio_datetime(self, df:pd.DataFrame)->pd.DataFrame:

        df['dt_inicio_exercicio'] = pd.to_datetime(df['dt_inicio_exercicio'], format ="%d/%m/%Y")

        return df
    
    def contribui_rpps(self, df:pd.DataFrame)->pd.DataFrame:

        df['contribui_rpps'] = df['dt_inicio_exercicio'].dt.year<2018
    
        return df


    def validate_df(self, df:pd.DataFrame)->pd.DataFrame:

        df = ServidorBaseDataframe.validate(df)

        return df


    def base_pipeline(self, df:pd.DataFrame)->pd.DataFrame:

        df = df.copy()
        df = self.renomear_colunas(df)
        df = self.obter_nivel_carreira(df)
        df = self.dt_inicio_exercicio_datetime(df)
        df = self.contribui_rpps(df)
        df = self.validate_df(df)

        return df

    def __call__(self, df:Optional[pd.DataFrame]=None)->pd.DataFrame:


        df_original = df or self.load_original_data()
        new_df = self.base_pipeline(df_original)
        
        return new_df

        


    

    


    


