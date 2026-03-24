from app.components.pipeline_status import PipelineStatus
from app.components.microdados import Microdados
from app.components.initial_pipeline_about import AboutSection
from app.state_manager import AppStateManager
from app.components.descriptor_df_original import DataSummaryComponent
from streamlit.delta_generator import DeltaGenerator
from core.simulator.initial_command import InitialCommand
import streamlit as st

class InitialPipelineSection:

    def __init__(self, container:DeltaGenerator)->None:

        self.pipeline = InitialCommand()
        self.microdados = Microdados()
        self.about_section = AboutSection()
        self.state = AppStateManager(namespace_name=self.pipeline.key, session_state=st.session_state)
        self.container= container

    def render(self)->None:

        with self.container:
            st.subheader("Sobre o tratamento dos dados")
            st.markdown("""Nesta seção, apresentamos o processo de carregamento e tratamento dos dados de servidores ativos, que é fundamental para a análise subsequente. O pipeline de dados é responsável por extrair, transformar e preparar os dados brutos para garantir sua qualidade e consistência. A seguir, detalhamos as etapas envolvidas nesse processo, destacando a importância de cada uma delas para a construção de uma base sólida para a análise dos reajustes salariais.""")
            with st.expander("Etapas do Pipeline de Dados"):
                container_etapas = st.container()
                self.about_section(container_etapas)
            container_pipeline = st.container()
            pipeline_status = PipelineStatus()
            state = pipeline_status(pipeline=self.pipeline, state=self.state, container=container_pipeline)
            container_df_final = st.container(border=True)
            with container_df_final:
                st.subheader("Dados originais tratados")
                st.write("Abaixo os dados tratrados podem ser explorados e é possível também fazer o download dos mesmos.")
            df_final = state.get_data('dados_finais')
            summary = DataSummaryComponent(df_final)
            self.microdados(df_final, data_name='Dados origignais tratados', 
                            explicacao=summary(),
                            component_container=container_df_final,
                            single_column=True)
            
    
    def __call__(self)->None:
        self.render()