import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from app.components.months_slider import SimulationMonthsSlider
from app.components.botao_trigger_simulacao import SimulationTrigger

class SimulationParametersSection:
    def __init__(self):
        # Instancia os componentes; os inits já cuidam do session_state
        self.months_slider = SimulationMonthsSlider(min_months=1, max_months=48)
        self.trigger = SimulationTrigger()

    @st.fragment
    def render(self) -> None:
        with st.container(border=True):
            # Container para o Slider
            slider_container = st.container()
            self.months_slider(slider_container)
            
            # Espaçamento entre componentes
            st.write("") 
            
            # Container para o Botão de Início
            trigger_container = st.container()
            self.trigger(trigger_container)

    def __call__(self) -> None:
        self.render()