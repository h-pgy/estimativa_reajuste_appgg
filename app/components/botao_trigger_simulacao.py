import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from app.state_manager import AppStateManager

class SimulationTrigger:
    def __init__(self, state_manager: AppStateManager) -> None:
        self.sm = state_manager
        self.__ensure_state()

    def __ensure_state(self) -> None:
        # Garante que a flag de execução existe no namespace
        try:
            self.sm.get_flag("run_pipeline")
        except KeyError:
            self.sm.set_flag("run_pipeline", False)

    def render(self, container: DeltaGenerator) -> None:
        with container:
            # Recupera o estado atual através do manager
            is_running = self.sm.get_flag("run_pipeline")
            
            if is_running:
                col_main, col_reset = st.columns([1, 1])
            else:
                _, col_main, _ = st.columns([1, 2, 1])

            with col_main:
                if st.button(
                    "Simulação Inicializada" if is_running else "Iniciar a simulação", 
                    type="primary", 
                    disabled=is_running,
                    use_container_width=True
                ):
                    # Define a flag no manager e dispara o rerun global
                    self.sm.set_flag("run_pipeline", True)
                    st.rerun() 
            
            if is_running:
                with col_reset:
                    if st.button(
                        "Reiniciar simulação", 
                        type="secondary",
                        use_container_width=True
                    ):
                        # Reseta a flag e reinicia o app
                        self.sm.set_flag("run_pipeline", False)
                        st.rerun()

    def __call__(self, container: DeltaGenerator) -> None:
        self.render(container)