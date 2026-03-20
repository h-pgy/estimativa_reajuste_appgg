from core.simulator.simulation_command import SimulationCommand, SimulationStep
from ..abstract_component import AbstractComponent
from ..component_item_model import ComponentItem
from streamlit.delta_generator import DeltaGenerator
from app.state_manager import AppStateManager
from typing import Callable, Generator
import time
import streamlit as st


class PipelineStatusComponent(AbstractComponent):

    def progress_bar(self, pipeline: SimulationCommand) -> Callable:

        qtd_steps = pipeline.num_steps
        step_size = 1/qtd_steps/2 #porque cada step tem 2 status relevantes: initialized e finished
        current_progress=0
        #define ela aqui dentro do container onde o componente vai existir para garantir que o progresso seja atualizado no mesmo componente, e não criando um novo a cada update
        with self.container:
            progress_bar = st.progress(current_progress, text=f"Iniciando pipeline: {pipeline.name}")
        
        #funcao aninhada porque consegue compartilhar o estado do progresso atual e do step size com Closure
        def update_progress(step: SimulationStep) -> None:
            
            nonlocal current_progress
            if step.initialized and not step.finished:
                current_progress+=step_size
                progress_bar.progress(current_progress, text=f"Step '{step.name}' iniciado.")
            if step.finished and step.sucess:
                current_progress+=step_size
                progress_bar.progress(current_progress, text=f"Step '{step.name}' finalizado com sucesso.")
            
            if step.error:
                #nesse caso não avança no current progress
                progress_bar.progress(current_progress, text=f"Step '{step.name}' finalizado com erro: {step.error_message}")

        
        return update_progress
    
            
    def prepare(self, pipeline: SimulationCommand, state_manager:AppStateManager) -> None:

        step_gen = pipeline.execute()
        update_progress_bar = self.progress_bar(pipeline)
        curr_step = None
        for step in step_gen:
            
            #primeira vez que estamos rodando o step, então escrevemos o nome dele
            if curr_step != step.key:
                curr_step = step.key
                self.add_item(ComponentItem(
                    args=[f"Step {step.name}"],
                    write_func=st.write
                ))
                #e atualizamos a barra de progresso porque ele se inicializou
                self.add_item(
                    ComponentItem(
                        args=[step],
                        write_func=update_progress_bar
                    )
                )
                    
            #ja rodamos ele antes, mas ele mudou de status, então atualizamos a barra de progresso
            # e checamos o status
            if curr_step == step.key:
                self.add_item(
                    ComponentItem(
                        args=[step],
                        write_func=update_progress_bar
                    )
                )
                if step.finished:
                    if step.error:
                        self.add_item(
                            ComponentItem(
                                args=[f"Step '{step.name}' finalizado com erro: {step.error_message}"],
                                write_func=st.error
                            )
                        )
                    if step.sucess:
                        self.add_item(
                            ComponentItem(
                                args=[f"Step '{step.name}' finalizado com sucesso."],
                                write_func=st.success
                            )
                        )
                        #e adicionamos o resultado no state manager
                        state_manager.set_flag(step.key+'_finished', True)
                        df = step.result
                        state_manager.set_data(step.key+'_result', df)
                        self.add_item(
                            ComponentItem(
                                args=[df],
                                write_func=st.dataframe
                            )
                        )
