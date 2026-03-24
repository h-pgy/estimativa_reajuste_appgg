import streamlit as st
from streamlit.delta_generator import DeltaGenerator
from config import LOGO_IMG

class Header:

    def render(self) -> None:
        cols = st.columns([1, 4], gap="small", vertical_alignment="center")
        with cols[0]:
            st.image(LOGO_IMG, width=150)
        with cols[1]:
            st.title("SimReajuste")
            st.subheader("Simulador de Impacto Orçamentário de Reajustes das Carreiras da Prefeitura de São Paulo")
            st.caption("Versão 1.0 | Desenvolvido pela APOGESP com foco na carreira de APPGG")
            st.divider()

    def __call__(self, container:DeltaGenerator)->None:

        with container:
            self.render()