import streamlit as st
from app.sections.initial_pipeline import InitialPipelineSection

st.header("Hell World - APP Simulador Reajuste Salarial Prefeitura de São Paulo")

espaco1 = st.empty()
espaco2  = st.empty()

with espaco1.container():
    st.subheader("Teste de componente: MicrodataDfOriginal")

with espaco2.container():
    container_section = st.container()
    initial_section = InitialPipelineSection(container_section)
    initial_section()