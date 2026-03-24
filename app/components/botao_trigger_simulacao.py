import streamlit as st
from streamlit.delta_generator import DeltaGenerator

class SimulationTrigger:
    def __init__(self) -> None:
        if "run_pipeline" not in st.session_state:
            st.session_state.run_pipeline = False

    def render(self, container: DeltaGenerator) -> None:
        with container:
            # Removi o @st.fragment daqui. 
            # Para que o botão de "Iniciar" libere o resto do script, 
            # o Streamlit precisa rodar o arquivo de cima a baixo.
            
            is_running = st.session_state.run_pipeline
            
            if is_running:
                col_main, col_reset = st.columns([1, 1])
            else:
                _, col_main, _ = st.columns([1, 2, 1])

            with col_main:
                # Botão de Iniciar
                if st.button(
                    "Simulação Inicializada" if is_running else "Iniciar a simulação", 
                    type="primary", 
                    disabled=is_running
                ):
                    st.session_state.run_pipeline = True
                    st.rerun() # Agora ele dá trigger no script todo
            
            if is_running:
                with col_reset:
                    # Botão de Reiniciar
                    if st.button("Reiniciar simulação", type="secondary"):
                        st.session_state.run_pipeline = False
                        st.rerun()

    def __call__(self, container: DeltaGenerator) -> None:
        self.render(container)