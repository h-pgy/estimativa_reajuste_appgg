from .simulation_command import SimulationCommand
from .steps.initial import load_original_data, make_sintetic_recem_nomeados_data, prepare_original_data
from core.utils.json import load_json
from config import CARGO_BASE, TABELA_ORIGINAL, QTD_RECEM_NOMEADOS

class InitialCommand(SimulationCommand):

    def __init__(self, fpath_tabela_original:str=TABELA_ORIGINAL, qtd_recem_nomeados:int=QTD_RECEM_NOMEADOS) -> None:
        super().__init__()
        self.tabela_original = load_json(fpath_tabela_original)
        self.qtd_recem_nomeados = qtd_recem_nomeados
        self.load_steps()

    def load_steps(self)->None:

        self.add_step('Cargamento dos dados originais', 
                      'Carregando os dados originais dos servidores no Portal de Dados Abertos', 
                      load_original_data)
        
        self.add_step('Limpando dados originais',
                      'Preparando os dados originais dos servidores para análise',
                      prepare_original_data,
                      args={'df_tabela_original':self.tabela_original})
        
        self.add_step('Gerando dados sintéticos de recém nomeados',
                      f'Gerando dados sintéticos dos servidores da carreira {CARGO_BASE} recém nomeados que ainda não estão no portal de Dados Abertos',
                      make_sintetic_recem_nomeados_data,
                      args={'qtd_servidores' : self.qtd_recem_nomeados}
                      )