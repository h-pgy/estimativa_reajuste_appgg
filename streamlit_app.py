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
if not st.session_state.run_pipeline:
    with cta_placeholder.container():
        _, col_btn, _ = st.columns([1, 2, 1])
        with col_btn:
            if st.button("Iniciar a simulação", type="primary", use_container_width=True):
                st.session_state.run_pipeline = True
                st.rerun()  

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