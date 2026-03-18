from core.utils.calculadora_inflacao import CalculadoraFatorInflacao
from core.models.tabelas import NivelTabela, TabelaDataframe
from core.utils.json import load_json_to_dataframe
from typing import Optional
import os
import pandas as pd

class TabelaFactory:

    def __init__(self) -> None:

        self.calculadora_inflacao = CalculadoraFatorInflacao()

    def validar_tabela(self, df:pd.DataFrame)->pd.DataFrame:

        df = TabelaDataframe.validate(df)        
        df = self.validar_tabela(df)


        return df

    def carregar_tabela(self, filepath:str)->pd.DataFrame:

        if not os.path.exists(filepath):
            raise ValueError('O arquivo especificado não existe.')
        df = load_json_to_dataframe(filepath)
        df = self.validar_tabela(df)

        return df
    
    def criar_tabela_from_dict(self, table_dict:list[dict])->pd.DataFrame:

        valid_data = []
        for nivel in table_dict:
            valid_nivel = NivelTabela(**nivel)
            valid_data.append(valid_nivel.dict())
        
        df = pd.DataFrame(valid_data)
        df = self.validar_tabela(df)

        return df

    def obter_fator_inflacao(self, indice:str, data_inicial:str, data_final:str)->float:

        if indice not in self.calculadora_inflacao.INDICES:
            raise ValueError(f"Índice de inflação '{indice}' não disponível. Índices disponíveis: {self.calculadora_inflacao.INDICES}")

        return self.calculadora_inflacao(data_inicial, data_final)
    
    def atualizar_inflacao(self, tabela:pd.DataFrame, indice:str, data_inicial:str, data_final:str)->pd.DataFrame:


        fator = self.obter_fator_inflacao(indice, data_inicial, data_final)
        df = tabela.copy(deep=True)
        df['remuneracao'] = df['remuneracao'] * fator
        df = self.validar_tabela(df)

        return df

    def solve_tabela_original(self, filepath:Optional[str], table_dict:Optional[list[dict]])->pd.DataFrame:

        if filepath:
            df = self.carregar_tabela(filepath)
        elif table_dict:
            df = self.criar_tabela_from_dict(table_dict)
        else:
            raise ValueError("É necessário fornecer um arquivo ou um dicionário para criar a tabela.")

        return df

    def pipelne(self, filepath:Optional[str], table_dict:Optional[list[dict]], indice:Optional[str], 
                data_inicial:Optional[str], data_final:Optional[str])->pd.DataFrame:

        df = self.solve_tabela_original(filepath, table_dict)

        if indice is not None:
            if data_inicial is None or data_final is None:
                raise ValueError("Para atualizar a tabela com inflação, é necessário fornecer as datas inicial e final.")
            df = self.atualizar_inflacao(df, indice, data_inicial, data_final)

        return df

    def __call__(self, filepath:Optional[str], table_dict:Optional[list[dict]], indice:Optional[str], 
                data_inicial:Optional[str], data_final:Optional[str])->pd.DataFrame:

        return self.pipelne(filepath, table_dict, indice, data_inicial, data_final)