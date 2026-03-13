from .simulation_command import SimulationCommand
from steps.initial import load_original_data, make_sintetic_recem_nomeados_data, prepare_original_data
from config import CARGO_BASE

class InitialCommand(SimulationCommand):

    def __init__(self) -> None:
        super().__init__()
        self.load_steps()

    def load_steps(self)->None:

        self.add_step('Cargamento dos dados originais', 
                      'Carregando os dados originais dos servidores no Portal de Dados Abertos', 
                      load_original_data)
        
        self.add_step('Limpando dados originais',
                      'Preparando os dados originais dos servidores para análise',
                      prepare_original_data)
        
        self.add_step('Gerando dados sintéticos de recém nomeados',
                      f'Gerando dados sintéticos dos servidores da carreira {CARGO_BASE} recém nomeados que ainda não estão no portal de Dados Abertos',
                      make_sintetic_recem_nomeados_data)