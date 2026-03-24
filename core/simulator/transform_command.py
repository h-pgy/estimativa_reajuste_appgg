from .simulation_command import SimulationCommand
from .steps.transform import (
    Vencimento, #vencimento precisa ser instanciado com a tabela específica
    calc_decimo_terceiro,
    calc_terco_adicional,
    calc_vale_alimentacao,
    calc_contrib_iprem,
    calc_contrib_inss,
    calc_prev_complementar,
    total_mensal
)
from core.models.tabelas import TabelaDataframe
from core.models.servidores import ServidorBaseDataframe
import pandas as pd

from config import VALOR_VALE_ALIMENTACAO, SALARIO_MINIMO, TETO_INSS, ALIQUOTA_COMPLEMENTAR, ALIQUOTA_INSS, CONTRIBUICAO_IPREM

class ProjectionCommand(SimulationCommand):

    def __init__(self, df_servidores_limpo:pd.DataFrame, tabela_projetada:pd.DataFrame, mes_projecao:int) -> None:
        
        df_servidores_limpo = ServidorBaseDataframe.validate(df_servidores_limpo)
        nome = "Projeção dos gastos mensais com os servidores"
        super().__init__(name=nome, initial_df=df_servidores_limpo)
        self.tabela_projetada = TabelaDataframe.validate(tabela_projetada)
        self.mes_projecao = mes_projecao
        self.load_steps()

    def load_steps(self)->None:

        self.add_step("Calculando o vencimento atual dos servidores",
                      'calc_vencimento',
                      "Cálculo do vencimento atual dos servidores com base na tabela projetada e no nível projetado para o mês",
                      Vencimento(self.tabela_projetada),
                      args={"mes_serie" : self.mes_projecao}
                      )
        self.add_step("Calculando o décimo terceiro salário",
                      'calc_decimo_terc',
                      "Cálculo do décimo terceiro dos servidores em base mensal, correspondente a 1/12 do vencimento atual projetado",
                      calc_decimo_terceiro)
        self.add_step("Calculando o terço adicional de férias",
                      'calc_ferias',
                      "Cálculo do terço adicional de férias em base mensal, correspondente a 1/3 do vencimento atual projetado",
                      calc_terco_adicional)
        self.add_step("Calculando o vale alimentação",
                      'calc_vale_alimentacao',
                      f"Cálculo do vale alimentação, no valor de {VALOR_VALE_ALIMENTACAO}, que é devido aos servidores que ganham menos de 10 salários mínimos (valor de {SALARIO_MINIMO})",
                      calc_vale_alimentacao)
        self.add_step("Calculando o valor da contribuição para o IPREM",
                      'calc_contrib_iprem',
                      f"Calculando a contribuição para o IPREM, com a alíquota de {CONTRIBUICAO_IPREM} apenas para os servidores ingressantes antes de 2018",
                      calc_contrib_iprem)
        self.add_step("Calculando a contribuição para o INSS",
                      'calc_contrib_inss',
                      f"Calculando a contribuição para o INSS, com a alíquota de {ALIQUOTA_INSS} tendo como valor base máximo o teto do INSS (valor de {TETO_INSS}) e igressaram após 2018",
                      calc_contrib_inss)
        self.add_step("Calculando a contribuição para a previdência complementar",
                      'calc_prev_complementar',
                        f"Calculando a contribuição para a previdência complementar, com a alíquota de {ALIQUOTA_COMPLEMENTAR} para os servidores que ganham acima do teto do INSS (valor de {TETO_INSS}), tendo como valor base o vencimento menos o teto do INSS, e ingressaram após 2018",
                        calc_prev_complementar)
        self.add_step("Cálculo dos encargos totais mensais",
                      'calc_total_mensal',
                      "Cálculo do total mensal de gastos da prefeitura com o servidor, considerando os gastos elencados anteriormente, que estão vinculados ao vencimento",
                      total_mensal)