import streamlit as st
from streamlit.delta_generator import DeltaGenerator

class SimulationMonthsSlider:
    def __init__(self, min_months: int = 1, max_months: int = 48) -> None:
        self.min = min_months
        self.max = max_months
        if "simulation_months" not in st.session_state:
            st.session_state.simulation_months = self.min

    @property
    def label_markdown(self) -> str:
        return f"Selecione a quantidade de meses para a simulação (o valor mínimo é {self.min} e o máximo é {self.max})."

    def render(self, container: DeltaGenerator) -> None:
        with container:
            # Verifica se a simulação já foi disparada para aplicar o bloqueio
            is_disabled = st.session_state.get("run_pipeline", False)
            
            st.markdown(self.label_markdown)
            
            st.slider(
                label="Meses de simulação",
                min_value=self.min,
                max_value=self.max,
                key="simulation_months",
                label_visibility="collapsed",
                disabled=is_disabled
            )

            # Exibe o sucesso apenas quando a simulação está ativa
            if is_disabled:
                st.success(
                    f"Simulação configurada para {st.session_state.simulation_months} meses.", 
                    icon="⏳"
                )

    def __call__(self, container: DeltaGenerator) -> None:
        self.render(container)