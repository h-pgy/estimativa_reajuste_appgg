import streamlit as st
from app.sections.test import test_microdata_df_original

st.header("Hell World - APP Simulador Reajuste Salarial Prefeitura de São Paulo")

espaco1 = st.empty()

with espaco1.container():
    st.subheader("Teste de componente: MicrodataDfOriginal")
    test_microdata_df_original(st.container())