from abc import ABC, abstractmethod
import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from core.utils.str import to_snake_case
from .component_item_model import ComponentItem

class AbstractComponent(ABC):

    def __init__(self, parent_container:DeltaGenerator, key_suffix:str='', **layout_kwargs)->None:

        self.parent_container = parent_container
        nome_classe = self.__class__.__name__
        #must pass a unique suffix if instantiating the same component multiple times in an app
        self.key = to_snake_case(nome_classe)+f"_{key_suffix}"
        self.container = st.container(key=self.key, **layout_kwargs)
        self.itens = []

    def add_item(self, item: ComponentItem) -> None:
        self.itens.append(item)

    def write(self, item: ComponentItem) -> None:

        with self.container:
            item.write_func(*item.args, **item.kwargs)

    @abstractmethod
    def prepare(self, *args, **kwargs) -> None:
        pass

    def render(self, *args, **kwargs)->None:

        self.prepare(*args, **kwargs)
        with self.parent_container:
            for item in self.itens:
                self.write(item)

    def __call__(self, *args, **kwargs)->None:

        self.render(*args, **kwargs)

