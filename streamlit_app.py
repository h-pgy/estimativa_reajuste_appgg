import streamlit as st
from app.sections.initial_pipeline import InitialPipelineSection
from app.sections.about import AboutSection
from app.sections.header import HeaderSection

st.set_page_config(
    layout="wide", 
    page_title="SimReajuste - APPGG SP",
    page_icon=":chart_with_upwards_trend:"
)

nav_items = [
    {"label": "📊 Sobre o Projeto", "anchor": "sobre-o-simreajuste"},
    {"label": "⚙️ Dados e Pipeline", "anchor": "carregamento-e-tratamento-dos-dados-de-servidores-ativos"}
]

header = st.empty()
sobre = st.empty()
pipeline_inicial  = st.empty()

with header.container():
    container_section = st.container()
    header_section = HeaderSection(container_section, nav_items)
    header_section()

with sobre.container():
    container_section = st.container(border=True)
    with container_section:
        st.header('Sobre o SimReajuste')
    about_section = AboutSection(container_section)
    about_section()

with pipeline_inicial.container():
    container_section = st.container(border=True)
    with container_section:
        st.header('Carregamento e tratamento dos dados de servidores ativos.')
    initial_section = InitialPipelineSection(container_section)
    initial_section()