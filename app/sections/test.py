from app.components.concret_components import MicrodataDfOriginal
from app.components.concret_components import StepStatusComponent
from core.simulator.initial_command import InitialCommand
import streamlit as st

def test_microdata_df_original(parent_container):

    with parent_container:
        pipeline = InitialCommand()
        step_gen = pipeline.execute()
        num_steps = pipeline.num_steps
        progress_step = 1/num_steps
        progress_percent = 0
        i = 0
        progress_bar = st.progress(progress_percent, text="Iniciando carregamento dos dados originais")
        while i < num_steps:
            step = next(step_gen)
            print(f'Step {i} iniciado. Step name: {step.name}. Statsus: {step.current_status}')
            st.write(step.name)
            component = StepStatusComponent(st.empty(), key_suffix=step.key+f'_{i}_{step.current_status}')
            component(step)
    
            if step.sucess:
                i+=1
                progress_percent+=progress_step
                progress_bar.progress(progress_percent, text=f"Step '{step.name}' finalizado com sucesso")
                df = step.result
                component = MicrodataDfOriginal(st.empty(), key_suffix=step.key)
                component(df)


