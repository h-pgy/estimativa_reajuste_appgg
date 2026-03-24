import streamlit as st
from streamlit.delta_generator import DeltaGenerator

class AboutSection:


    @property
    def step_extraction(self) -> dict:
        return {
            "summary": "Extração de dados oficiais da Relação de Servidores Ativos da PMSP.",
            "details": """
            Os dados são extraídos da [Relação de Servidores Ativos da Prefeitura](https://dados.prefeitura.sp.gov.br/dataset/servidores-ativos-da-prefeitura), 
            disponível no Portal de Dados Abertos. O sistema utiliza o recorte de **fevereiro de 2026**, que contém informações funcionais de 
            todos os servidores da administração direta.
            """
        }

    @property
    def step_filtering(self) -> dict:
        return {
            "summary": "Filtragem e seleção de escopo para a carreira de APPGG.",
            "details": """
            Dada a magnitude da base municipal, o pipeline isola exclusivamente os registros de interesse. 
            Neste estágio, selecionamos apenas os servidores da carreira de **Analista de Políticas Públicas e Gestão Governamental (APPGG)**, 
            garantindo que as simulações foquem na estrutura específica desta categoria.
            """
        }

    @property
    def step_validation(self) -> dict:
        return {
            "summary": "Validação de contrato e tipagem para garantia de integridade.",
            "details": """
            O sistema executa checagens de consistência para garantir a integridade da simulação. **Exemplos de validações:**
            * **Integridade de Registros:** Verificação se os Registros Funcionais (RFs) mantêm o padrão de sete dígitos.
            * **Consistência de Campos:** Obrigatoriedade de preenchimento de campos nominais e identificadores únicos.
            * **Padronização:** Uniformização de nomenclaturas e seleção das variáveis (*Nome, RF, Cargo, Secretaria e Exercício*).
            """
        }

    @property
    def step_feature_engineering(self) -> dict:
        return {
            "summary": "Saneamento e criação de novas features de negócio (ex: Regra Previdenciária).",
            "details": """
            Os dados brutos são convertidos em tipos computáveis e enriquecidos. **Exemplos de transformações:**
            * **Normalização Temporal:** Conversão da data de exercício para `datetime`, requisito para o cálculo de interstícios.
            * **Lógica Previdenciária:** Identificação da contribuição ao **RPPS** baseada no marco de 2018. Esta é apenas uma das diversas variáveis calculadas para mensurar encargos patronais com precisão.
            * **Cálculo da data de início de exercício corrigida:** Alguns servidores não se encontram atualmente no nível em que deveriam estar de acordo com sua data de início de exercício, pois tiveram eventos funcionais que interromperam a contagme do tempo. A data de início de exercício corrigida desconta esses eventos funcionais, somando os dias à data de início de exercício, o que permite posteriormente fazer um cálculo muito mais preciso da evolução do servidores na carreira.
            """
        }

    @property
    def step_synthetic_data(self) -> dict:
        return {
            "summary": "Expansão da base com dados sintéticos para simulação prospectiva.",
            "details": """
            O pipeline injeta **dados sintéticos** representando servidores em processo de nomeação. Como estes profissionais 
            ainda não constam no Portal de Dados Abertos, essa etapa é vital para prever o impacto orçamentário real após a posse dos novos quadros.
            """
        }

    def render(self, container: DeltaGenerator) -> None:
        with container:
            
            # Renderização dos passos com Expander
            steps = [
                self.step_extraction,
                self.step_filtering,
                self.step_validation,
                self.step_feature_engineering,
                self.step_synthetic_data
            ]
            
            for i, step in enumerate(steps, 1):
                with st.expander(f"**{i}.** {step['summary']}"):
                    st.markdown(step['details'])
            
            st.info("A tabela apresentada na seção seguinte exibe o resultado final deste tratamento.")

    def __call__(self, container: DeltaGenerator) -> None:
        self.render(container)