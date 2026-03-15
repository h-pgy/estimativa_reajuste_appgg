from core.models.servidores import ServidorVencimentoDataframe
import pandas as pd

class TotalMensal:

    colunas_total = [
        'vencimento',
        'decimo_terceiro',
        'terco_ferias',
        'contribuicao_iprem',
        'contribuicao_inss',
        'previdencia_complementar',
        'vale_alimentacao'
    ]

    
    def __call__(self, df:pd.DataFrame)->pd.DataFrame:

        df = ServidorVencimentoDataframe.validate(df)

        for col in self.colunas_total:
            if col not in df.columns:
                raise ValueError(f'Precisa calcular {col} antes.')

        df['valor_total'] = df[self.colunas_total].sum(axis=1)
        
        return df