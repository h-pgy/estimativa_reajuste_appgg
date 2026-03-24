import streamlit as st
from streamlit.delta_generator import DeltaGenerator

class Navbar:
    def __init__(self, sections: list[dict]) -> None:
        self.sections = sections

    @property
    def css(self) -> str:
        # Usamos 'fixed' e definimos a largura como 100%
        # O background-color usa a variável do Streamlit para respeitar o Dark Mode
        return """
        <style>
            /* Container da Navbar Fixa */
            .nav-container {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 60px;
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 20px;
                background-color: var(--secondary-background-color);
                border-bottom: 1px solid rgba(128, 128, 128, 0.2);
                z-index: 999999;
                box-shadow: 0px 2px 10px rgba(0,0,0,0.1);
            }
            
            .nav-item {
                text-decoration: none !important;
                color: var(--text-color) !important;
                font-weight: 500;
                padding: 8px 16px;
                border-radius: 8px;
                transition: all 0.3s ease;
                font-size: 14px;
            }
            
            .nav-item:hover {
                background-color: var(--primary-color);
                color: white !important;
            }

            /* HACK: O Streamlit tem um padding-top nativo. 
               Como a barra é fixa, precisamos garantir que o conteúdo 
               não comece "atrás" dela. Ajustamos o bloco principal. */
            .main .block-container {
                padding-top: 80px !important;
            }
            
            /* Remove o header padrão do Streamlit (opcional, para ficar mais limpo) */
            header[data-testid="stHeader"] {
                display: none;
            }
        </style>
        """

    def render(self, container: DeltaGenerator) -> None:
        # Injetamos o CSS globalmente para que o padding afete a página toda
        st.markdown(self.css, unsafe_allow_html=True)
        
        # HTML da Navbar
        nav_html = '<div class="nav-container">'
        for section in self.sections:
            nav_html += f'<a class="nav-item" href="#{section["anchor"]}">{section["label"]}</a>'
        nav_html += '</div>'
        
        # Renderizamos a div
        st.markdown(nav_html, unsafe_allow_html=True)

    def __call__(self, container: DeltaGenerator) -> None:
        self.render(container)