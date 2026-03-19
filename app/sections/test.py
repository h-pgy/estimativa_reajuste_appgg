from app.components.concret_components import MicrodataDfOriginal
from core.simulator.initial_command import InitialCommand
import streamlit as st

def test_microdata_df_original(parent_container):

    with parent_container:
        pipeline = InitialCommand()
        for step in pipeline.execute():
            if step.initialized and not step.finished:
                st.write(f"Step {step.name} initialized but not finished.")
            if step.finished and step.sucess:
                st.write(f"Step {step.name} finished.")
                df = step.result
            if step.finished and step.error:
                st.write(f"Step {step.name} finished with error: {step.error_message}")
        
        if step.sucess:
            component = MicrodataDfOriginal(parent_container)
            component(df)


