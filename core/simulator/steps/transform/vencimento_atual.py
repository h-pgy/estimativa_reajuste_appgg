from core.utils.datetime import meses_passados, adicionar_meses
from core.models.servidores import ServidorBaseDataframe, ServidorBase, ServidorVencimentoDataframe
from core.models.tabelas import TabelaDataframe
from pandera.typing import Series
from datetime import datetime
import pandas as pd

class Vencimento:

    def __init__(self, tabela_vencimento:pd.DataFrame)->None:

        self.tabela_vencimento = TabelaDataframe.validate(tabela_vencimento)

    def tempo_exercicio_meses_total(self, dt_inicio_exercicio_corrigida:datetime, mes_serie:int)->int:

        hoje = datetime.today()
        data_projetada = adicionar_meses(dt_inicio_exercicio_corrigida, mes_serie)

        return meses_passados(hoje, data_projetada)
    
    def meses_cumulativo(self, tabela_vencimento:pd.DataFrame)->pd.DataFrame:

        #precisa dar shift aqui porque o acumulado de meses para o nível 1 é 0, ou seja, a pessoa precisa ter 0 meses de exercício para alcançar o nível 1,
        #  X meses para alcançar o nível 2, onde X é o tempo máximo que você fica no nível 1, e assim por diante
        tabela_vencimento['qtd_meses_acumulado'] = tabela_vencimento['qtd_meses_no_nivel'].cumsum().shift(1, fill_value=0)

        return tabela_vencimento
    

    def nivel_projetado(self, row:Series[ServidorBase], mes_serie:int)->int:

        tempo_exercicio_meses = self.tempo_exercicio_meses_total(row['dt_inicio_exercicio_corrigida'], mes_serie)
        tabela_vencimento = self.meses_cumulativo(self.tabela_vencimento)

        #filtra a tabela para apenas os niveis que a pessoa alcançou, ou seja aqueles cujo qtd_meses_acumulado é
        # menor ou igual ao tempo de exercício em meses
        tabela_vencimento_niveis_alcancados = tabela_vencimento[
            tabela_vencimento['qtd_meses_acumulado'] <= tempo_exercicio_meses].reset_index(drop=True)

        # pega o nivel máximo alcançado, que é o nível projetado para aquela pessoa naquele mês da série
        nivel = tabela_vencimento_niveis_alcancados['nivel'].max()

        if pd.isnull(nivel):
            nivel = 1

        return int(nivel)
    
    def obter_vencimento(self, row:Series[ServidorBase])->float:

        nivel = row['nivel_projetado']
        # pega a remuneração correspondente ao nível projetado
        vencimento: float = self.tabela_vencimento[self.tabela_vencimento['nivel'] == nivel]['remuneracao'].values[0]
        return vencimento

    def pipeline(self, df:pd.DataFrame, mes_serie:int)->pd.DataFrame:

        df = ServidorBaseDataframe.validate(df)
        df['nivel_projetado'] = df.apply(lambda row: self.nivel_projetado(row, mes_serie), axis=1)
        df['vencimento'] = df.apply(self.obter_vencimento, axis=1)

        return df
    
    def __call__(self, df:pd.DataFrame, mes_serie:int)->pd.DataFrame:

        df = self.pipeline(df, mes_serie)
        #df = ServidorVencimentoDataframe.validate(df)

        return df

        

        