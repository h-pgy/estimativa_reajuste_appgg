from app.components.concret_components import PipelineStatusComponent
from core.simulator.initial_command import InitialCommand
import streamlit as st
from app.state_manager import AppStateManager
import time

def test_microdata_df_original(parent_container):

    state = AppStateManager('initial_pipeline', st.session_state)
    with parent_container:
        initial_pipeline = InitialCommand()
        status = PipelineStatusComponent(parent_container)
        status(initial_pipeline, state)


