from core.models.simulation_step import SimulationStep
from ..abstract_component import AbstractComponent
from ..component_item_model import ComponentItem
from streamlit.delta_generator import DeltaGenerator
import streamlit as st
import time


class StepStatusComponent(AbstractComponent):

    def spinner(self, message:str):
        with st.spinner(message):
            #hack so spinner will show even if it runs fast
            time.sleep(1)
            

    def solve_status(self, step:SimulationStep)->ComponentItem:

        if step.initialized and not step.finished:
            return ComponentItem(
                args=[f"Step {step.name} initialized."],
                write_func=self.spinner
            )
        if step.finished and step.sucess:
            return ComponentItem(
                args=[f"Step {step.name} finished."],
                write_func=st.success
            )

        if step.finished and step.error:
            return ComponentItem(
                args=[f"Step {step.name} finished with error: {step.error_message}"],
                write_func=st.error
            )
        
        raise RuntimeError('Status do step não identificado')
    
    def prepare(self, step: SimulationStep) -> None:

        status_component = self.solve_status(step)
        self.add_item(status_component)

    