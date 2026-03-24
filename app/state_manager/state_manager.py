import streamlit as st
import pandas as pd
from .session_state_model import SessionStateNamespace
from core.models.simulation_step import SimulationStep
from streamlit.runtime.state.session_state_proxy import SessionStateProxy
from collections import OrderedDict
from pydantic import TypeAdapter

class AppStateManager:

    def __init__(self, namespace_name:str, session_state: SessionStateProxy)->None:

        self.__namespace_name = namespace_name
        self.check_session_state = TypeAdapter(SessionStateNamespace).validate_python
        self.namespace: SessionStateNamespace = self.__initialize_namespace(namespace_name, session_state)

    @property
    def namespace_name(self) -> str:
        return self.__namespace_name
    
    def __is_SessionStateObj(self, obj:object)->bool:

        try:
            self.check_session_state(obj)
            return True
        except Exception as e:
            print(f'Erro ao validar objeto como SessionStateNamespace: {e}')
            return False

    def __setattr__(self, nome, valor):

        if nome == 'namespace':
            if not self.__is_SessionStateObj(valor):
                raise ValueError('O valor atribuído a namespace deve ser uma instância de SessionStateNamespace.')

        if nome == 'namespace_name' and hasattr(self, 'namespace_name'):
            raise AttributeError('O atributo namespace_name é somente leitura e não pode ser modificado após a inicialização.')
        
        super().__setattr__(nome, valor)

    def __get_saved_namespace(self, namespace_name:str, state:SessionStateProxy)->SessionStateNamespace:
        saved_namespace = state[namespace_name]
        
        if not isinstance(saved_namespace, (dict, OrderedDict)):
            saved_namespace = saved_namespace.model_dump() if hasattr(saved_namespace, 'model_dump') else saved_namespace.__dict__
        
        return SessionStateNamespace(**saved_namespace)

    def __initialize_namespace(self, namespace_name:str, state:SessionStateProxy)->SessionStateNamespace:

        if namespace_name in state:
            namespace_obj = self.__get_saved_namespace(namespace_name, state)
        else:
            namespace_obj = SessionStateNamespace(name=namespace_name, data=OrderedDict(), steps=OrderedDict(), flags=OrderedDict())
        state[namespace_name] = namespace_obj
        
        return namespace_obj
    
    def get_data(self, key:str)->pd.DataFrame:
        
        if key not in self.namespace.data:
            raise KeyError(f'Chave "{key}" não encontrada no namespace "{self.namespace_name}".')
        return self.namespace.data[key]

    def set_data(self, key:str, value:pd.DataFrame)->None:
        if not isinstance(value, pd.DataFrame):
            raise ValueError('O valor atribuído deve ser um DataFrame do pandas.')
        self.namespace.data[key] = value

    def get_step(self, key:str)->SimulationStep:
        
        if key not in self.namespace.steps:
            raise KeyError(f'Chave "{key}" não encontrada no namespace "{self.namespace_name}".')
        
        return self.namespace.steps[key]
        
    def add_step(self, step:SimulationStep)->SimulationStep:

        if not isinstance(step, SimulationStep):
            raise ValueError('Step must be a SimulationStep object')
        key = step.key
        if key in self.namespace.steps:
            return self.get_step(key)
        self.namespace.steps[key] = step
        return step
    
    @property
    def current_step(self) -> SimulationStep | None:
        last_key = list(self.namespace.steps.keys())[-1] if self.namespace.steps else None
        if last_key is None:
            return None
        return self.get_step(last_key)
    
    def is_current_step(self, step:SimulationStep)->bool:

        current_step = self.current_step
        if current_step is None:
            return False
        return current_step.key == step.key
    
    def set_flag(self, flag_name:str, value:bool)->None:
        if not isinstance(value, bool):
            raise ValueError('O valor do flag deve ser do tipo booleano.')
        self.namespace.flags[flag_name] = value

    def get_flag(self, flag_name:str)->bool:
        if flag_name not in self.namespace.flags:
            raise KeyError(f'Flag "{flag_name}" não encontrada no namespace "{self.namespace_name}".')
        return self.namespace.flags[flag_name]
    

