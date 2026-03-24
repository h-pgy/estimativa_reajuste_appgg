import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from app.state_manager import AppStateManager
from app.components.tabela_remuneracao import SalaryTableEditor
from app.components.months_slider import SimulationMonthsSlider
from app.components.botao_trigger_simulacao import SimulationTrigger

class SimulationParametersSection:
    def __init__(self, namespace: str = "simulacao_v1"):
        # A Seção é a dona do estado
        self.sm = AppStateManager(namespace_name=namespace, session_state=st.session_state)
        
        # Injeção do state manager nos componentes filhos
        self.table_editor = SalaryTableEditor(self.sm)
        self.months_slider = SimulationMonthsSlider(self.sm)
        self.trigger = SimulationTrigger(self.sm)

    @st.fragment
    def render(self) -> None:
        with st.container(border=True):
            st.subheader("Configurações da Simulação")
            
            # 1. Editor de Tabela (Base de Dados)
            self.table_editor(st.container())
            
            st.divider()
            
            # 2. Slider de Meses (Constante de Tempo)
            self.months_slider(st.container())
            
            st.write("") 
            
            # 3. Trigger (Botão Iniciar/Reset)
            self.trigger(st.container())

    def __call__(self) -> AppStateManager:
        self.render()
        # Retorna o gestor para que o script principal 
        # acesse os dados validados (tabela, meses, etc)
        return self.sm