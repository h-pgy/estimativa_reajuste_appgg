from core.utils.datetime import meses_passados, adicionar_meses
from core.models.tabelas import TabelaDataframe
import pandas as pd
from datetime import datetime

class CorrectDtInicioExercicio:

    def __init__(self, df_tabela_original:pd.DataFrame)->None:

        self.tabela_original = TabelaDataframe.validate(df_tabela_original)

    def meses_passados_inicio_exercicio(self, dt_inicio_exercicio:datetime)->int:

        hoje = datetime.today()

        return meses_passados(hoje, dt_inicio_exercicio)
    
    def qtd_meses_acumulado_nivel(self, nivel:int)->int:

        niveis_anteriores = self.tabela_original[self.tabela_original['nivel']<nivel].reset_index(drop=True)
        total_meses_ate_nivel = niveis_anteriores['qtd_meses_acumulado'].max()

        return total_meses_ate_nivel
    
    def meses_a_ajustar(self, dt_inicio_exercicio:datetime, nivel:int)->int:

        meses_passados = self.meses_passados_inicio_exercicio(dt_inicio_exercicio)
        meses_acumulados_prox_nivel = self.qtd_meses_acumulado_nivel(nivel+1)

        #nesse caso ele deveria ter passado para o próximo nível mas não passou
        #a unica forma disso ter ocorrido é se ele teve meses que nao foram efetivo exercicio
        #entao precisamos "remover" esses niveis do calculo, 
        # ou seja, ajustar a data de início de exercício corrigida para uma data mais recente
        if meses_passados > meses_acumulados_prox_nivel:
            return meses_passados - meses_acumulados_prox_nivel
        else:
            return 0
        
    def ajustar_dt_inicio_exercicio(self, row:pd.Series)->datetime:

        dt_inicio_exercicio = row['dt_inicio_exercicio']
        nivel_atual = row['nivel']

        meses_a_ajustar = self.meses_a_ajustar(dt_inicio_exercicio, nivel_atual)

        if meses_a_ajustar == 0:
            return dt_inicio_exercicio
        
        dt_inicio_exercicio_corrigida = adicionar_meses(dt_inicio_exercicio, meses_a_ajustar)

        return dt_inicio_exercicio_corrigida

    
    def __call__(self, df:pd.DataFrame)->pd.DataFrame:

        df = df.copy()

        df['dt_inicio_exercicio_corrigida'] = df.apply(self.ajustar_dt_inicio_exercicio, axis=1)

        return df

