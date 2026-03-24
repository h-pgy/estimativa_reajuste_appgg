import streamlit as st
from app.sections.initial_pipeline import InitialPipelineSection
from app.sections.about import AboutSection
from app.sections.header import HeaderSection
from app.sections.start_simulation import SimulationParametersSection

st.set_page_config(
    layout="wide", 
    page_title="SimReajuste - APPGG SP",
    page_icon=":chart_with_upwards_trend:"
)

nav_items = [
    {"label": "📊 Sobre o Projeto", "anchor": "sim-reajuste"},
    {"label": "⚙️ Parâmetros da Simulação", "anchor": "parametros-da-simulacao"},
    {"label": "🛠️ Dados Originais", "anchor": "carregamento-e-tratamento-dos-dados-de-servidores-ativos"}
]

# 2. Inicialização do Session State
if "run_pipeline" not in st.session_state:
    st.session_state.run_pipeline = False

header = st.empty()
sobre = st.empty()
cta_placeholder = st.empty()
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

# Lógica do Botão (SÓ APARECE SE NÃO FOI CLICADO)
with cta_placeholder.container():
    container_section = st.container(border=True)
    with container_section:
        st.header("Parâmetros da Simulação")
        params_section = SimulationParametersSection()
        params_section()

if st.session_state.run_pipeline:
    with pipeline_inicial.container():
        container_section = st.container(border=True)
        with container_section:
            st.header('Carregamento e tratamento dos dados de servidores ativos.')
        initial_section = InitialPipelineSection(container_section)
        initial_section()

else:
    with pipeline_inicial.container():
        st.info("Clique no botão acima para carregar os dados e iniciar o pipeline.")