import streamlit as st
import pandas as pd
from .session_state_model import SessionState
from streamlit.runtime.state.session_state_proxy import SessionStateProxy

class AppStateManager:

    def __init__(self, namespace:str, session_state: SessionStateProxy)->None:

        self.namespace = self.initialize_namespace(namespace, session_state)

    def initialize_namespace(self, namespace:str, state:SessionStateProxy)->None:

        if state.get(namespace) is None:
            state[namespace] = {}

        if not isinstance(state[namespace], dict):
            raise ValueError('Namespace já existe e não é um dicionário.')
        return state[namespace]
    



