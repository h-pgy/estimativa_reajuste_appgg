from ..abstract_component import AbstractComponent
from ..component_item_model import ComponentItem
import pandas as pd
import streamlit as st
from streamlit.delta_generator import DeltaGenerator


class MicrodataDfOriginal(AbstractComponent):

    def build_explicacao_pop_over(self) -> None:

        explicacao = """
        ### Dados dos Servidores (APPGG) - Portal de Dados Abertos

        Este dataframe representa os **dados originais** dos servidores buscados no **Portal de Dados Abertos**. 

        Os dados dos servidores ativos mais atualizados da prefeitura disponíveis nesse portal foram filtrados para obter todos os membros da carreira de **APPGGs**. Para fins de análise e identificação, foram extraídos os seguintes campos:

        * **Nome do Servidor:** Para identificação individual.
        * **Nível da Carreira:** Posicionamento em que o APPGG se encontra (ou se encontrava) no momento do registro no portal.
        * **Data de Início de Exercício:** Registro cronológico do ingresso na municipalidade.
        * **Sigla da Secretaria:** Sigla da secretaria em que o APPGG está (ou estava) lotado, fornecendo contexto sobre a área de atuação.

        > **Nota:** Esta base serve como referência primária para a identificação do custo orçamentário atual de manutenção da carreira e para simulação do impacto orçamentário de reajustes aplicados sobre a tabela.
        """

        with st.expander("Detalhes sobre a tabela:"):
            st.markdown(explicacao)

    def prepare(self, df:pd.DataFrame) -> None:


        df_item = ComponentItem(
            args=[df],
            write_func=st.dataframe
        )

        expander_explicacao = ComponentItem(
            write_func=self.build_explicacao_pop_over
        )

        self.add_item(df_item)
        self.add_item(expander_explicacao)

