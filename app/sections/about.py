from app.components.hero import Hero
from app.components.header import Header
import streamlit as st
from config import HEADER_IMG

class AboutSection:

    def __init__(self, container) -> None:
        self.container = container
        self.hero = Hero()

    def render(self) -> None:

        with self.container:
            with st.container():
                cols = st.columns(2, gap="medium", vertical_alignment="top")
                with cols[0]:
                    container_img = st.container(border=True)
                    container_img.image(HEADER_IMG, width="stretch")
                with cols[1]:
                    container_header = st.container()
                    self.hero(container_header)

    def __call__(self) -> None:
        self.render()