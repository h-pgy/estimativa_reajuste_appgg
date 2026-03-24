import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from app.components.header import Header

class HeaderSection:


    def __init__(self, container:DeltaGenerator):

        self.container = container
        self.header = Header()

    def render(self)->None:

        with self.container:
            header_container = st.container()
            self.header(header_container)

    def __call__(self) -> None:
        self.render()

