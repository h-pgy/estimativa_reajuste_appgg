from core.models.servidores import ServidorBase, ServidorBaseDataframe
from datetime import datetime
import pandas as pd
from typing import List
from config import CARGO_BASE, DT_NOMEACAO

class RecemNomeadoData:

    def __init__(self, dt_nomeacao:datetime=DT_NOMEACAO, cargo_base:str=CARGO_BASE)->None:

        self.dt_nomeacao = dt_nomeacao 

        if not cargo_base[-1].isdigit():
            cargo_base += '1'
        
        self.cargo_base = cargo_base
        self.rpps = self.dt_nomeacao.year<2018

    def fake_rf(self, numero:int)->str:

        return str(numero).zfill(7)

    def fake_name(self, numero:int)->str:

        return f'recem_nomeado_{numero}'

    def generate_servidor(self, numero:int)->ServidorBase:

        servidor = ServidorBase(
            rf = self.fake_rf(numero),
            nome = self.fake_name(numero),
            cargo_base = self.cargo_base,
            secretaria='NA',
            nivel=1,
            dt_inicio_exercicio=self.dt_nomeacao,
            dt_inicio_exercicio_corrigida=self.dt_nomeacao,
            rpps=self.rpps
        )

        return servidor
    
    def generate_servidores(self, qtd:int)->List[ServidorBase]:

        servidor_lst = []
        for i in range(qtd):
            numero = i+1
            servidor = self.generate_servidor(numero)
            servidor_lst.append(servidor)

        return servidor_lst
    
    def servidores_to_df(self, servidor_lst:List[ServidorBase])->pd.DataFrame:

        data = [
            servidor.model_dump()
            for servidor in servidor_lst
        ]

        df = pd.DataFrame(data)

        return df
    
    def validate_dataframe(self,df:pd.DataFrame)->pd.DataFrame:

        df = ServidorBaseDataframe.validate(df)

        return df

    
    def pipeline(self, qtd_servidores:int)->pd.DataFrame:


        data = self.generate_servidores(qtd_servidores)
        df = self.servidores_to_df(data)
        df = self.validate_dataframe(df)

        return df
    
    def __call__(self, df:pd.DataFrame, qtd_servidores:int)->pd.DataFrame:


        original_df = ServidorBaseDataframe.validate(df)
        servidores_sinteticos = self.pipeline(qtd_servidores)
        df_final = pd.concat([original_df, servidores_sinteticos])
        df_final = df_final.reset_index(drop=True)

        return df_final



    