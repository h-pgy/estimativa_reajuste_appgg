import streamlit as st
from streamlit.delta_generator import DeltaGenerator
import pandas as pd
import io

@st.fragment
def download_button(csv_data:bytes, data_name:str)->bool:
    return st.download_button(label="Faça Download dos Dados", data=csv_data, file_name=f"{data_name}.csv", mime="text/csv")

class Microdados:

    def exibir_sumario_tecnico(self, container: DeltaGenerator, df: pd.DataFrame):
        # Construção do DataFrame de metadados
        df_info = pd.DataFrame({
            'Coluna': df.columns,
            'Tipo de Dado': df.dtypes.values.astype(str),
            'Valores Não Nulos': df.count().values,
            'Valores Nulos': df.isna().sum().values,
            '% de Nulos': (df.isna().sum().values / len(df) * 100).round(2)
        })
        
        # Renderização no Streamlit
        container.subheader("Sumário Técnico do Conjunto de Dados")
        container.dataframe(df_info, hide_index=True, use_container_width=True)
        
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

    def pipeline(self, df:pd.DataFrame, data_name:str, explicacao:str, component_container:DeltaGenerator, single_column:bool)->None:

        with component_container:
            if not single_column:
                col_df, col_buttons = st.columns(2)
                self.render_dataframe(df, col_df)
                self.add_explicacao(explicacao, col_buttons)
                with st.spinner('Salvando os dados em csv...'):
                    self.download_as_csv_button(df, data_name, col_buttons)
            else:
                self.render_dataframe(df, component_container)
                with st.spinner('Salvando os dados em csv...'):
                    self.download_as_csv_button(df, data_name, component_container)
                self.add_explicacao(explicacao, component_container)
                

    def __call__(self, df:pd.DataFrame, data_name:str, explicacao:str, component_container:DeltaGenerator, single_column:bool=False)->None:
        self.pipeline(df, data_name, explicacao, component_container, single_column)