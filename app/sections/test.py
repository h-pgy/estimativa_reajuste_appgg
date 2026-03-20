from app.components.pipeline_status import PipelineStatus
from app.components.microdados import Microdados
from app.state_manager import AppStateManager
from streamlit.delta_generator import DeltaGenerator
from core.simulator.initial_command import InitialCommand
import streamlit as st

class InitialPipelineSection:

    def __init__(self, container:DeltaGenerator)->None:

        self.pipeline = InitialCommand()
        self.state = AppStateManager(namespace_name=self.pipeline.key, session_state=st.session_state)
        self.container= container

    def render(self)->None:

        pipeline_status = PipelineStatus()
        state = pipeline_status.status_pipeline(pipeline=self.pipeline, state=self.state, container=self.container)
    
    def __call__(self)->None:
        self.render()