import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from app.state_manager import AppStateManager

class SimulationMonthsSlider:
    def __init__(self, state_manager: AppStateManager, min_months: int = 1, max_months: int = 48) -> None:
        self.sm = state_manager
        self.min = min_months
        self.max = max_months
        self.slider_key = f"slider_months_{self.sm.namespace_name}"
        self.__ensure_state()

    def __ensure_state(self) -> None:
        # Agora usando set_constant para os meses
        try:
            self.sm.get_constant("simulation_months")
        except KeyError:
            self.sm.set_constant("simulation_months", self.min)
            
        # Garante que a flag de execução existe para o disable
        try:
            self.sm.get_flag("run_pipeline")
        except KeyError:
            self.sm.set_flag("run_pipeline", False)

    def _update_manager(self):
        # Sincroniza o valor do widget com o constants do AppStateManager
        novo_valor = st.session_state[self.slider_key]
        self.sm.set_constant("simulation_months", novo_valor)

    @property
    def label_markdown(self) -> str:
        return f"Selecione a quantidade de meses para a simulação (mínimo: {self.min}, máximo: {self.max})."

    def render(self, container: DeltaGenerator) -> None:
        with container:
            # Recupera estado do manager
            is_disabled = self.sm.get_flag("run_pipeline")
            # Busca especificamente em constants
            valor_atual = self.sm.get_constant("simulation_months")
            
            st.markdown(self.label_markdown)
            
            st.slider(
                label="Meses de simulação",
                min_value=self.min,
                max_value=self.max,
                value=valor_atual,
                key=self.slider_key,
                on_change=self._update_manager,
                label_visibility="collapsed",
                disabled=is_disabled
            )

            if is_disabled:
                st.success(
                    f"Simulação configurada para {valor_atual} meses.", 
                    icon="⏳"
                )

    def __call__(self, container: DeltaGenerator) -> None:
        self.render(container)