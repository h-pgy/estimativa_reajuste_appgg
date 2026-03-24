import streamlit as st
import pandas as pd
from streamlit.delta_generator import DeltaGenerator
from app.state_manager import AppStateManager
from core.simulator.tabela_factory import TabelaFactory
from core.models.tabelas import TabelaDataframe
from config import TABELA_ORIGINAL

class SalaryTableEditor:
    def __init__(self, state_manager:AppStateManager, filename: str=TABELA_ORIGINAL) -> None:
        self.sm = state_manager
        self.fpath_table = filename
        # Instancia a factory internamente
        self.factory = TabelaFactory()
        self.editor_key = f"editor_{self.sm.namespace_name}"
        self.__ensure_state()

    def __ensure_state(self) -> None:
        # Garante a existência da tabela no namespace do AppStateManager
        try:
            self.sm.get_data("salary_table")
        except KeyError:
            # Carrega via factory apenas na primeira vez
            df_inicial = self.factory(filepath=self.fpath_table)
            self.sm.set_data("salary_table", df_inicial)
        
        # Inicializa flags de controle no namespace
        for flag, default in [("is_editing", False), ("table_finalized", False)]:
            try:
                self.sm.get_flag(flag)
            except KeyError:
                self.sm.set_flag(flag, default)

    def _entrar_modo_edicao(self) -> None:
        self.sm.set_flag("is_editing", True)

    def _salvar_e_validar(self) -> None:
        # Recupera os dados do widget via Session State do Streamlit
        if self.editor_key in st.session_state:
            # O data_editor pode retornar um objeto complexo ou o DF diretamente
            state_value = st.session_state[self.editor_key]
            
            # Se houve edições manuais, o Streamlit retorna um dicionário de mudanças.
            # No entanto, a forma mais segura de pegar o DF final é via a própria key do widget
            # que o Streamlit sincroniza.
            df_editado = state_value
            
            try:
                # Validação Pandera (TabelaDataframe)
                validated_df = TabelaDataframe.validate(df_editado)
                
                # Persiste no AppStateManager
                self.sm.set_data("salary_table", validated_df)
                self.sm.set_flag("table_finalized", True)
                self.sm.set_flag("is_editing", False)
            except Exception as e:
                st.error(f"Erro na validação dos dados: {e}")

    @st.fragment
    def render(self) -> None:
        with st.container():
            is_editing = self.sm.get_flag("is_editing")
            is_finalized = self.sm.get_flag("table_finalized")
            df_current = self.sm.get_data("salary_table")

            col_table, col_text = st.columns([2, 1])

            with col_table:
                if is_editing and not is_finalized:
                    # O data_editor sincroniza automaticamente com a key
                    st.data_editor(
                        df_current,
                        width='stretch',
                        num_rows="dynamic",
                        key=self.editor_key
                    )
                else:
                    st.dataframe(df_current, use_container_width=True)

            with col_text:
                st.markdown("### Base Salarial")
                st.write("Esta tabela define as referências para o cálculo do impacto orçamentário.")
                
                # Botão Alterar
                st.button(
                    "Alterar tabela",
                    type="secondary",
                    disabled=is_editing or is_finalized,
                    on_click=self._entrar_modo_edicao,
                    use_container_width=True
                )

                # Botão Salvar
                if is_editing and not is_finalized:
                    st.button(
                        "Salvar e Validar",
                        type="primary",
                        on_click=self._salvar_e_validar,
                        use_container_width=True
                    )
                
                if is_finalized:
                    st.success("Tabela validada com sucesso!", icon="✅")
                    # Botão opcional para desfazer o bloqueio (caso precise)
                    if st.button("Refazer alterações", type="tertiary"):
                        self.sm.set_flag("table_finalized", False)
                        self.sm.set_flag("is_editing", True)
                        st.rerun()

    def __call__(self, container: DeltaGenerator)-> None:

        with container:
            self.render()