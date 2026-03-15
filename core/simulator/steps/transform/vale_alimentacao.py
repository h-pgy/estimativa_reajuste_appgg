from core.models.servidores import ServidorVencimento
import pandas as pd
from pandera.typing import Series
from config import VALOR_VALE_ALIMENTACAO, SALARIO_MINIMO

class ValeAlimentacao:


    def __init__(self, valor_va:float=VALOR_VALE_ALIMENTACAO, salario_minimo:float=SALARIO_MINIMO)->None:

        self.valor_va = valor_va
        self.salario_minimo = salario_minimo

    def calcular_va(self, row:Series[ServidorVencimento])->float:

        vencimento = row['vencimento']
        limite_va = self.salario_minimo * 10

        if vencimento < limite_va:
            return self.valor_va
        return 0.0
    
    def __call__(self, df:pd.DataFrame)->pd.DataFrame:

        df['vale_alimentacao'] = df.apply(self.calcular_va, axis=1)
        
        return df