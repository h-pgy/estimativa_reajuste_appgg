import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from app.components.header import Header
from app.components.navbar import Navbar

class HeaderSection:


    def __init__(self, container:DeltaGenerator, sections_dict:list[dict]):

        self.container = container
        self.header = Header()
        self.navbar = Navbar(sections_dict)

    def render(self)->None:

        with self.container:
            navbar_container=st.container(border=True)
            self.navbar(navbar_container)
            header_container = st.container()
            self.header(header_container)

    def __call__(self) -> None:
        self.render()

