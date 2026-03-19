import streamlit as st
import pandas as pd
from .session_state_model import SessionStateNamespace
from streamlit.runtime.state.session_state_proxy import SessionStateProxy

class AppStateManager:

    def __init__(self, namespace_name:str, session_state: SessionStateProxy)->None:

        self.__namespace_name = namespace_name
        self.namespace: SessionStateNamespace = self.__initialize_namespace(session_state)

    @property
    def namespace_name(self) -> str:
        return self.__namespace_name

    def __setattr__(self, nome, valor):

        if nome == 'namespace':
            if not isinstance(valor, SessionStateNamespace):
                raise ValueError('O valor atribuído a namespace deve ser uma instância de SessionStateNamespace.')

        if nome == 'namespace_name':
            raise AttributeError('O atributo namespace_name é somente leitura e não pode ser modificado após a inicialização.')

    def __initialize_namespace(self, state:SessionStateProxy)->SessionStateNamespace:

        if self.namespace_name in state:
            raise ValueError('Namespace já existe no session state. Escolha um nome diferente para evitar conflitos.')
        namespace_obj = SessionStateNamespace(name=self.namespace_name, data={}, steps=[], flags={})
        state[self.namespace_name] = namespace_obj
        
        return namespace_obj
    
    def get_data(self, key:str)->pd.DataFrame:
        
        if key not in self.namespace.data:
            raise KeyError(f'Chave "{key}" não encontrada no namespace "{self.namespace_name}".')
        return self.namespace.data[key]

    def set_data(self, key:str, value:pd.DataFrame)->None:
        if not isinstance(value, pd.DataFrame):
            raise ValueError('O valor atribuído deve ser um DataFrame do pandas.')
        self.namespace.data[key] = value

    def add_step(self, step_name:str)->None:
        if step_name in self.namespace.steps:
            raise ValueError(f'Step "{step_name}" já existe no namespace "{self.namespace_name}".')
        self.namespace.steps.append(step_name)

    @property
    def current_step(self) -> str | None:
        return self.namespace.steps[-1] if self.namespace.steps else None
    
    def get_step(self, posit:int)->str:
        if posit < 0 or posit >= len(self.namespace.steps):
            raise IndexError(f'Posição {posit} está fora dos limites da lista de steps.')
        return self.namespace.steps[posit]
    
    def set_flag(self, flag_name:str, value:bool)->None:
        if not isinstance(value, bool):
            raise ValueError('O valor do flag deve ser do tipo booleano.')
        self.namespace.flags[flag_name] = value

    def get_flag(self, flag_name:str)->bool:
        if flag_name not in self.namespace.flags:
            raise KeyError(f'Flag "{flag_name}" não encontrada no namespace "{self.namespace_name}".')
        return self.namespace.flags[flag_name]
    

