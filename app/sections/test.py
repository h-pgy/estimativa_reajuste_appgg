from app.components.concret_components import MicrodataDfOriginal
from app.components.concret_components import StepStatusComponent
from core.models.simulation_step import SimulationStep
from core.simulator.initial_command import InitialCommand
import streamlit as st
import time

def test_microdata_df_original(parent_container):

    with parent_container:
        pipeline = InitialCommand()
        step_gen = pipeline.execute()
        num_steps = pipeline.num_steps
        progress_step = 1/num_steps
        progress_percent = 0
        i = 0
        progress_bar = st.progress(progress_percent, text="Iniciando carregamento dos dados originais")
        curr_key = None
        while i < num_steps:
            step: SimulationStep = next(step_gen)
            if curr_key != step.key:
                space = st.empty()
                curr_key = step.key
                st.write(step.name)
            print(f'Step {i} iniciado. Step name: {step.name}. Statsus: {step.current_status}')
            component = StepStatusComponent(space, key_suffix=step.key+f'_{i}_{step.current_status}')
            component(step)
            if step.current_status=='initialized':
                time.sleep(3)
            
            if step.sucess:
                i+=1
                progress_percent+=progress_step
                progress_bar.progress(progress_percent, text=f"Step '{step.name}' finalizado com sucesso")
                df = step.result
                component = MicrodataDfOriginal(st.empty(), key_suffix=step.key)
                component(df)


