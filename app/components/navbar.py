import streamlit as st
from streamlit.delta_generator import DeltaGenerator

class Navbar:
    def __init__(self, sections: list[dict]) -> None:
        self.sections = sections

    @property
    def css(self) -> str:
        return """
        <style>
            .nav-container {
                display: flex;
                justify-content: center;
                gap: 15px;
                padding: 12px;
                /* Usa a cor de fundo secundária do tema atual (Light ou Dark) */
                background-color: var(--secondary-background-color);
                border-radius: 12px;
                margin-bottom: 30px;
                border: 1px solid rgba(128, 128, 128, 0.2);
            }
            .nav-item {
                text-decoration: none !important;
                /* Usa a cor de texto padrão do tema atual */
                color: var(--text-color) !important;
                font-weight: 500;
                padding: 8px 20px;
                border-radius: 8px;
                transition: all 0.3s ease;
                font-size: 14px;
            }
            .nav-item:hover {
                /* Usa a cor primária definida no tema (geralmente vermelho/laranja ou custom) */
                background-color: var(--primary-color);
                color: white !important;
                transform: translateY(-2px);
            }
        </style>
        """

    def render(self, container: DeltaGenerator) -> None:
        with container:
            st.markdown(self.css, unsafe_allow_html=True)
            
            nav_html = '<div class="nav-container">'
            for section in self.sections:
                nav_html += f'<a class="nav-item" href="#{section["anchor"]}">{section["label"]}</a>'
            nav_html += '</div>'
            
            st.markdown(nav_html, unsafe_allow_html=True)

    def __call__(self, container: DeltaGenerator) -> None:
        self.render(container)