from core.models.servidores import ServidorVencimento
import pandas as pd
from pandera.typing import Series

class DecimoTerceiro:

    def calcular_decimo_terceiro(self, row:Series[ServidorVencimento])->float:

        return round(row['vencimento']/12, 2)
    
    def __call__(self, df:pd.DataFrame)->pd.DataFrame:

        df['decimo_terceiro'] = df.apply(self.calcular_decimo_terceiro, axis=1)

        return df
    
class TercoAdicionalFerias:

    def calcular_terco_adicional(self, row:Series[ServidorVencimento])->float:

        return round(row['vencimento']/3, 2)
    
    def __call__(self, df:pd.DataFrame)->pd.DataFrame:

        df['terco_ferias'] = df.apply(self.calcular_terco_adicional, axis=1)

        return df