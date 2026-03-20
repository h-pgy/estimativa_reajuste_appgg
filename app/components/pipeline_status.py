import streamlit as st
from streamlit.delta_generator import DeltaGenerator
import pandas as pd
from typing import Generator
from app.state_manager import AppStateManager
from core.simulator.simulation_command import SimulationCommand, SimulationStep
import time

class PipelineStatus:

    def status_pipeline(self, pipeline:SimulationCommand, state:AppStateManager, container:DeltaGenerator)->AppStateManager:

        with container:
            st.markdown(f"#### {pipeline.name}")
            progress=0
            progress_bar = st.progress(0)
            qtd_steps = pipeline.num_steps
            step_size = 1/qtd_steps
            step_gen = pipeline.execute()
            with st.status("Preparando execução...", expanded=True) as status:
                for i in range(qtd_steps):
                    with st.container(border=True):
                        cols = st.columns(2)
                        with st.spinner(f"Executando o processo {i+1} de {qtd_steps}..."):
                            #hack para aparecer na UI
                            time.sleep(2)
                            step = next(step_gen)
                            state.add_step(step.key)
                            if step.initialized and not step.finished:
                                with cols[0]:
                                    st.info(f'{step.name} iniciado.')
                                step = next(step_gen)
                            if step.finished:
                                i += 1
                                progress+=step_size
                                progress_bar.progress(progress)
                                with cols[1]:
                                    if step.error:
                                        st.error(f'Erro no processo {step.name}: {step.error}')
                                        status.update(label = "Erro na execução!", state="error")
                                        break
                                    if step.sucess:
                                        st.success(f'{step.name} finalizado com sucesso!')
                                        state.set_data(step.key, step.result)
            time.sleep(2)
            status.update(label = "Execução finalizada!", state="complete")
        return state

    def __call__(self, pipeline:SimulationCommand, state:AppStateManager, container:DeltaGenerator)->AppStateManager:

        return self.status_pipeline(pipeline, state, container)
                    


        
    
    
