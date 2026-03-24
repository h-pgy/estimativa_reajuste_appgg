import streamlit as st
from streamlit.delta_generator import DeltaGenerator

class Hero:

    @property
    def definition_content(self) -> str:
        return """
        O **SimReajuste** é uma ferramenta de simulação desenvolvida para calcular o impacto orçamentário decorrente da aplicação 
        de reajustes sobre as tabelas remuneratórios das carreiras públicas efetivas, com base em 
        **microdados reais dos servidores ativos** da Prefeitura de São Paulo. O objetivo central é 
        oferecer transparência e precisão técnica nas negociações, permitindo que os gestores simulem, com base em evidência,
        o custo efetivo de propostas de valorização profissional considerando a progressão na carreira dos servidores.
        """

    @property
    def methodology_paragraphs(self) -> tuple[str, str]:
        p1 = """
        O simulador resolve a complexidade de projetar o impacto orçamentário da aplicação de reajustes em carreiras com distribuições desiguais entre os níveis, 
        incorporando ainda o fato de que os servidores progridem na carreira ao longo do tempo. Ele permite quantificar e simular em até **48 meses** o impacto de reajustes, considerando a evolução da pirâmide funcional e a progressão dos servidores, 
        e permitindo aplicar reajustes com base em **três** métodos distintos:
        1. **Índices Inflacionários:** Correção baseada no IPCA acumulado em diferentes períodos históricos.
        2. **Equiparação de Tabelas:** Unificação com estruturas de outras carreiras.
        3. **Tabelas ad hoc:** Definição de uma nova estrutura de vencimentos do zero, com base em parâmetros definidos pelo usuário.
        .
        """
        p2 = """
        Ao processar o momento exato em 
        que cada membro da carreira, considerando seu nível atual e a data de início de exercício, pode passar para o próximo nível, o SimReajuste
        é capaz de gerar uma estimativa bastante precisa do impacto orçamentário da aplicação de reajustes nas tabelas remuneratórias.
        Com base nos dados dessa simulação, o sistema realiza agregações que permitem identificar o gasto total por nível e por exercício financeiro, 
        considerando um horizonte de até 48 meses e comparando com a situação atual projetada. Além dissso, ele permite visualizar a evolução da 
        série histórica do impacto ao longo do tempo, permintindo uma melhor compreensão dos efeitos complexos da aplicação de reajustes sobre carreiras com diferentes 
        distribuições dos servidores nos níveis.
        """

        return (p1, p2)
    
    @property
    def context(self)->str:

        return """O sistema foi desenvolvido pela APOGESP, para subsidiar, com base em evidências, a tomada de decisão em relação à
        **campanha de reajuste salarial da carreira dos Analistas de Políticas Públicas (APPGG)** para o ano de 2026. sistema possui arquitetura 
        No entanto, ele possui arquitetura modular e pode ser configurado para calcular o impacto orçamentário do reajuste de qualquer carreira efetiva do município.
        """

    @property
    def simulation_modes(self) -> list[dict]:
        return [
            {
                "icon": ":chart_with_downwards_trend:",
                "title": "Índices Inflacionários",
                "caption": "Correção baseada no índice acumulado em períodos definidos pelo usuário (extraído diretamente da API do Banco Central) ."
            },
            {
                "icon": ":arrows_counterclockwise:",
                "title": "Equiparação de Tabelas",
                "caption": "Unificação com estruturas de outras carreiras já existente na Prefeitura."
            },
            {
                "icon": ":new:",
                "title": "Tabelas Ad Hoc",
                "caption": "Criação e simulação de uma nova estrutura de vencimentos do zero com inputs do usuário."
            }
        ]

    @property
    def methodology_details(self) -> str:
        return """
        #### Detalhamento Técnico
        A principal inovação do SimReajuste é abandonar projeções lineares simples em favor de um 
        **modelo dinâmico de progressão**. Diferente de cálculos estáticos, o sistema:
        
        1. **Mapeamento de Encargos:** Identifica os encargos variáveis vinculados diretamente ao vencimento de cada servidor.
        2. **Simulação de Interstícios:** Projeta a evolução individual por tempo de serviço (ex: progressões a cada 18 meses). Se um servidor atinge o tempo necessário no 3º mês da simulação, o sistema altera sua base de cálculo automaticamente a partir daquele ponto.
        3. **Horizonte Temporal:** Calcula o custo exato mês a mês em uma janela de até **48 meses**, cobrindo o período de uma gestão municipal completa.
        4. **Análise de Impacto:** Gera métricas agregadas que permitem identificar o gasto total por nível e por exercício financeiro.
        
        Esta abordagem permite visualizar o impacto real em carreiras com distribuições desiguais entre os níveis (pirâmides funcionais dinâmicas).
        """

    def render(self, container: DeltaGenerator) -> None:
        with container:            
            # Renderiza Textos Principais
            st.subheader("Sobre")
            st.markdown(self.definition_content)
            st.subheader("Metodologia")
            st.markdown(self.methodology_paragraphs[0])
            # Renderiza Colunas de Modos
            cols = st.columns(len(self.simulation_modes))
            for col, mode in zip(cols, self.simulation_modes):
                with col:
                    st.markdown(f"{mode['icon']} **{mode['title']}**")
                    st.caption(mode['caption'])
            with st.expander("Mais informações sobre a metodologia...", expanded=False):
                st.markdown(self.methodology_paragraphs[1])
            st.subheader("Contexto")
            st.markdown(self.context)
            st.divider()

            # Renderiza Popover de Metodologia
            st.write("")
            with st.popover(":information_source: Detalhes técnicos sobre a simulação", use_container_width=True):
                st.markdown(self.methodology_details)
            
            st.divider()

    def __call__(self, container: DeltaGenerator) -> None:
        self.render(container)