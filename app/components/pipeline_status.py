import streamlit as st
from streamlit.delta_generator import DeltaGenerator
import pandas as pd
from typing import Generator
from app.state_manager import AppStateManager
from core.simulator.simulation_command import SimulationCommand, SimulationStep
from app.components.microdados import Microdados
import time

class PipelineStatus:

    def __init__(self)->None:

        self.microdados = Microdados()

    def initialized(self, step:SimulationStep)->None:
        
        st.info(f'{step.name} iniciado.')

    def error(self, step:SimulationStep, status_container:DeltaGenerator)->None:

        st.error(f'Erro no processo {step.name}: {step.error}')
        status_container.update(label = "Erro na execução!", state="error")

    def sucess(self, step:SimulationStep, state:AppStateManager)->None:

        st.success(f'{step.name} finalizado com sucesso!')
        state.set_data(step.key, step.result)#aqui tá errado é o objeto de state

    def render_data(self, step:SimulationStep)->None:

        with st.popover("Resumo dos dados"):
            self.microdados.exibir_sumario_tecnico(container=st.container(), df=step.result)
        with st.popover('Detalhar dados'):
            self.microdados(df=step.result, data_name=step.name, explicacao=step.message, component_container=st.container())


    def status_pipeline(self, pipeline:SimulationCommand, state:AppStateManager, container:DeltaGenerator)->AppStateManager:

        st.markdown(f"#### {pipeline.name}")
        progress=0
        progress_bar = st.progress(0)
        qtd_steps = pipeline.num_steps
        step_size = 1/qtd_steps
        step_gen = pipeline.execute()
        with st.status("Preparando execução...", expanded=True) as status:
            for i in range(qtd_steps):
                with st.container(border=True):
                    cols = st.columns(3)
                    with st.spinner(f"Executando o processo {i+1} de {qtd_steps}..."):
                        #hack para aparecer na UI
                        time.sleep(2)
                        step = next(step_gen)
                        state.add_step(step)
                        if step.initialized and not step.finished:
                            with cols[0]:
                                self.initialized(step)
                            step = next(step_gen)
                        if step.finished:
                            i += 1
                            progress+=step_size
                            progress_bar.progress(progress)
                            with cols[1]:
                                if step.error:
                                    self.error(step, status)
                                    break
                                if step.sucess:
                                    self.sucess(step, state)
                                    with cols[2]:
                                        self.render_data(step)

        time.sleep(2)
        status.update(label = "Execução finalizada! Clique aqui para acessar os detalhes", state="complete")
        return state

    def __call__(self, pipeline:SimulationCommand, state:AppStateManager, container:DeltaGenerator)->AppStateManager:

        with container:
            internal_container = st.container(border=True)
            with internal_container:
                return self.status_pipeline(pipeline, state, container)
                    


        
    
    
