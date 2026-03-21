import streamlit as st
from streamlit.delta_generator import DeltaGenerator
import pandas as pd
import io

@st.fragment
def download_button(csv_data:bytes, data_name:str)->bool:
    return st.download_button(label="Faça Download dos Dados", data=csv_data, file_name=f"{data_name}.csv", mime="text/csv")

class Microdados:

    def renderizar_info_dataframe(self, container: DeltaGenerator, df: pd.DataFrame):
        # Captura a saída do df.info()
        buffer = io.StringIO()
        df.info(buf=buffer)
        s = buffer.getvalue()
        
        container.markdown("### Estrutura Técnica do Dataset")
        container.code(s, language="text")
    
    def render_dataframe(self, df:pd.DataFrame, container_df:DeltaGenerator)->None:

        with container_df:
            st.dataframe(df)

    def add_explicacao(self, explicacao:str, container_explicacao:DeltaGenerator)->None:

        with container_explicacao:
            st.markdown('#### Explicação dos Dados')
            st.markdown(explicacao)

    def download_as_csv(self, df:pd.DataFrame)->bytes:

        return df.to_csv(index=False).encode('utf-8')
    
    @st.fragment
    def download_as_csv_button(self, df:pd.DataFrame, data_name:str, button_container:DeltaGenerator)->None:

        with button_container:
            csv_data = self.download_as_csv(df)
            button = download_button(csv_data, data_name)

    def pipeline(self, df:pd.DataFrame, data_name:str, explicacao:str, component_container:DeltaGenerator)->None:

        with component_container:
            col_df, col_buttons = st.columns(2)
            self.render_dataframe(df, col_df)
            self.add_explicacao(explicacao, col_buttons)
            with st.spinner('Salvando os dados em csv...'):
                self.download_as_csv_button(df, data_name, col_buttons)

    def __call__(self, df:pd.DataFrame, data_name:str, explicacao:str, component_container:DeltaGenerator)->None:
        self.pipeline(df, data_name, explicacao, component_container)