from core.models.servidores import ServidorVencimento, ServidorVencimentoDataframe
import pandas as pd
from config import CONTRIBUICAO_IPREM, ALIQUOTA_INSS, TETO_INSS
from pandera.typing import Series

class ContribuicaoIprem:

    def __init__(self, contribuicao_iprem:float=CONTRIBUICAO_IPREM)->None:

        self.contribuicao_iprem = contribuicao_iprem

    def obter_valor_base(self, row:Series[ServidorVencimento])->float:

        # o iprem nao considera o terço adicional de férias
        valor_base = row['vencimento'] + row['decimo_terceiro']

        return valor_base

    def calcular_contribuicao_iprem(self, row:Series[ServidorVencimento])->float:

        if not row['rpss']:
            return 0.0
        
        valor_base = self.obter_valor_base(row)
        return round(valor_base * self.contribuicao_iprem, 2)
    
    def __call__(self, df:pd.DataFrame)->pd.DataFrame:

        df = ServidorVencimentoDataframe.validate(df)

        if 'decimo_terceiro' not in df.columns:
            raise ValueError('Precisa calcular o décimo terceiro antes.')

        df['contribuicao_iprem'] = df.apply(self.calcular_contribuicao_iprem, axis=1)

        return df