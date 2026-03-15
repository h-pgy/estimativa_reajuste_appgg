from core.models.servidores import ServidorVencimento
import pandas as pd
from config import CONTRIBUICAO_IPREM, ALIQUOTA_INSS, TETO_INSS, ALIQUOTA_COMPLEMENTAR
from pandera.typing import Series

class ContribuicaoIprem:

    def __init__(self, contribuicao_iprem:float=CONTRIBUICAO_IPREM)->None:

        self.contribuicao_iprem = contribuicao_iprem

    def obter_valor_base(self, row:Series[ServidorVencimento])->float:

        # o iprem nao considera o terço adicional de férias
        valor_base = row['vencimento'] + row['decimo_terceiro']

        return valor_base

    def calcular_contribuicao_iprem(self, row:Series[ServidorVencimento])->float:

        if not row['rpps']:
            return 0.0
        
        valor_base = self.obter_valor_base(row)
        return round(valor_base * self.contribuicao_iprem, 2)
    
    def __call__(self, df:pd.DataFrame)->pd.DataFrame:

        if 'decimo_terceiro' not in df.columns:
            raise ValueError('Precisa calcular o décimo terceiro antes.')

        df['contribuicao_iprem'] = df.apply(self.calcular_contribuicao_iprem, axis=1)

        return df
    
class ContribuicaoINSS:

    def __init__(self, aliquota_inss:float=ALIQUOTA_INSS, teto_inss:float=TETO_INSS)->None:

        self.aliquota_inss = aliquota_inss
        self.teto_inss = teto_inss

    def obter_valor_base(self, row:Series[ServidorVencimento])->float:

        # o inss vai sobre todos os vencimentos, incluso terco adicional
        valor_base = row['vencimento'] + row['terco_ferias'] + row['decimo_terceiro']

        # se der maior que o teto tem que ajustar para o teto
        if valor_base > self.teto_inss:
            valor_base = self.teto_inss

        return valor_base

    def calcular_contribuicao_inss(self, row:Series[ServidorVencimento])->float:

        if row['rpps']:
            return 0.0
        
        valor_base = self.obter_valor_base(row)
        return round(valor_base * self.aliquota_inss, 2)
    
    def __call__(self, df:pd.DataFrame)->pd.DataFrame:

        if 'decimo_terceiro' not in df.columns:
            raise ValueError('Precisa calcular o décimo terceiro antes.')
        if 'terco_ferias' not in df.columns:
            raise ValueError('Precisa calcular o terco adicional de férias antes.')

        df['contribuicao_inss'] = df.apply(self.calcular_contribuicao_inss, axis=1)

        return df
    

class PrevidenciaComplementar:

    def __init__(self, aliquota_complementar:float=CONTRIBUICAO_IPREM, teto_inss:float=TETO_INSS)->None:

        self.aliquota_complementar = aliquota_complementar
        self.teto_inss = teto_inss

    def obter_valor_base(self, row:Series[ServidorVencimento])->float:

        # a aliquota complementar é só sobre vencimento e decimo terceiro
        valor_base = row['vencimento'] + row['decimo_terceiro']

        return valor_base

    def calcular_previdencia_complementar(self, row:Series[ServidorVencimento])->float:

        if row['rpps']:
            return 0.0
        
        valor_base = self.obter_valor_base(row)
        return round(valor_base * self.aliquota_complementar, 2)
    
    def __call__(self, df:pd.DataFrame)->pd.DataFrame:

        if 'decimo_terceiro' not in df.columns:
            raise ValueError('Precisa calcular o décimo terceiro antes.')

        df['previdencia_complementar'] = df.apply(self.calcular_previdencia_complementar, axis=1)

        return df