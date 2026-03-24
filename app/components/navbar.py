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
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 60px;
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 20px;
                z-index: 999999;
                border-bottom: 1px solid rgba(128, 128, 128, 0.3);
                box-shadow: 0px 2px 10px rgba(0,0,0,0.2);
                margin: 0;
                padding: 0;
            }

            /* Modo Light */
            @media (prefers-color-scheme: light) {
                .nav-container {
                    background-color: #FFFFFF !important;
                }
                .nav-item {
                    color: #31333F !important;
                }
            }

            /* Modo Dark */
            @media (prefers-color-scheme: dark) {
                .nav-container {
                    background-color: #0E1117 !important;
                }
                .nav-item {
                    color: #FAFAFA !important;
                }
            }
            
            .nav-item {
                text-decoration: none !important;
                font-weight: 500;
                padding: 8px 16px;
                border-radius: 8px;
                transition: all 0.3s ease;
                font-size: 14px;
            }
            
            .nav-item:hover {
                background-color: var(--primary-color) !important;
                color: white !important;
            }

            .main .block-container {
                padding-top: 80px !important;
            }
            
            header[data-testid="stHeader"] {
                display: none !important;
            }
        </style>
        """

    def render(self, container: DeltaGenerator) -> None:
        st.markdown(self.css, unsafe_allow_html=True)
        
        nav_html = f'''
        <div class="nav-container">
            {''.join([f'<a class="nav-item" href="#{s["anchor"]}">{s["label"]}</a>' for s in self.sections])}
        </div>
        '''
        
        st.markdown(nav_html, unsafe_allow_html=True)

    def __call__(self, container: DeltaGenerator) -> None:
        self.render(container)