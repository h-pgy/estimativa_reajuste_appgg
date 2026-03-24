import pandas as pd
from .data_loader import Loader
from .correct_inicio_exercicio import CorrectDtInicioExercicio
from core.models.servidores import ServidorBaseDataframe
from core.models.tabelas import TabelaDataframe
from pandera.typing import DataFrame
from core.models.dados_originais_servidores import schema_dados_originais
from typing import Optional
from config import CARGO_BASE

class Preparator:

    def __init__(self, cargo_base:str=CARGO_BASE)->None:

        self.cargo_base = cargo_base
        self.load_original_data = Loader()



    def renomear_colunas(self, df:pd.DataFrame)->pd.DataFrame:

        renomear_cols = {
            'REGISTRO' : 'rf',
            'NOME' : 'nome',
            'REF_CARGO_BAS' : 'cargo_base',
            'SIGLA' : 'secretaria',
            'DATA_INICIO_EXERC' : 'dt_inicio_exercicio'
        }
        
        df = df.rename(renomear_cols, axis=1)

        df = df[list(renomear_cols.values())]

        return df

    def filtrar_para_membros_carreira(self, df:pd.DataFrame, cargo_base:str=CARGO_BASE)->pd.DataFrame:
        
        df['cargo_base'] = df['cargo_base'].fillna('Não informado').astype(str)
        df = df[df['cargo_base'].str.startswith(cargo_base)]
        df = df.reset_index(drop=True)

        return df
    
    def rf_to_str(self, df:pd.DataFrame)->pd.DataFrame:

        df['rf'] = df['rf'].astype(str).str.zfill(7)

        return df
    

    def obter_nivel_carreira(self, df:pd.DataFrame)->pd.DataFrame:

        df['nivel'] = df['cargo_base'].str.extract(r'(\d+)$').astype(int)

        return df
    
    def dt_inicio_exercicio_datetime(self, df:pd.DataFrame)->pd.DataFrame:

        df['dt_inicio_exercicio'] = pd.to_datetime(df['dt_inicio_exercicio'], format ="%d/%m/%Y")

        return df
    
    def contribui_rpps(self, df:pd.DataFrame)->pd.DataFrame:

        df['rpps'] = df['dt_inicio_exercicio'].dt.year<2018
    
        return df
    
    def validate_df(self, df:pd.DataFrame)->pd.DataFrame:

        df = ServidorBaseDataframe.validate(df)

        return df

    def base_pipeline(self, df:pd.DataFrame)->pd.DataFrame:

        df = df.copy()
        #valida se os dados estão ok
        df = schema_dados_originais.validate(df)
        df = self.renomear_colunas(df)
        df = self.rf_to_str(df)
        df = self.filtrar_para_membros_carreira(df, self.cargo_base)
        df = self.obter_nivel_carreira(df)
        df = self.dt_inicio_exercicio_datetime(df)
        df = self.contribui_rpps(df)
        df = self.corrigir_inicio_exercicio(df)
        df = self.validate_df(df)

        return df

    def __call__(self, df_tabela_original:pd.DataFrame, df:Optional[pd.DataFrame]=None)->pd.DataFrame:

        #ficou estranho mas é o jeito para funcionar com o padrão comand
        df_tabela_original = TabelaDataframe.validate(df_tabela_original)
        self.corrigir_inicio_exercicio = CorrectDtInicioExercicio(df_tabela_original)

        if df is None:
            df = self.load_original_data()
        df_original = df
        new_df = self.base_pipeline(df_original)
        
        return new_df

        


    

    


    


