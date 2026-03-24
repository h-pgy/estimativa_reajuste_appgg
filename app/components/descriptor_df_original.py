import streamlit as st
import pandas as pd
from streamlit.delta_generator import DeltaGenerator

class DataSummaryComponent:
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    @property
    def total_servidores(self) -> int:
        return len(self.df)

    @property
    def n_secretarias(self) -> int:
        return self.df['secretaria'].nunique()

    @property
    def carreira_info(self) -> dict:
        return {
            "n_niveis": self.df['nivel'].nunique(),
            "min": self.df['nivel'].min(),
            "max": self.df['nivel'].max()
        }

    @property
    def contagem_origem(self) -> dict:
        # Identifica sintéticos pelo padrão 'recem_nomeado' no nome
        mask_sintetico = self.df['nome'].str.contains('recem_nomeado', na=False)
        n_sinteticos = len(self.df[mask_sintetico])
        return {
            "sinteticos": n_sinteticos,
            "reais": self.total_servidores - n_sinteticos
        }

    @property
    def n_rpps(self) -> int:
        return int(self.df['rpps'].sum())

    @property
    def markdown_content(self) -> str:
        return f"""
##### Descrição do Dataset Processado

A base de dados resultante do pipeline constitui a relação consolidada de servidores da carreira de APPGG. O arquivo processado contém **{self.total_servidores}** registros estruturados para subsidiar a modelagem de impacto financeiro.

###### Composição da Base
* **Servidores Reais:** {self.contagem_origem['reais']} registros extraídos do Portal de Dados Abertos.
* **Servidores Sintéticos:** {self.contagem_origem['sinteticos']} registros (identificados como `recem_nomeado`) inseridos para simular futuras nomeações.
* **Diversidade Institucional:** Servidores alocados em **{self.n_secretarias}** unidades administrativas distintas da prefeitura.

###### Estrutura da Carreira e Previdência
* **Níveis Funcionais:** A amostra abrange **{self.carreira_info['n_niveis']}** níveis funcionais, situados entre o nível {self.carreira_info['min']} e o nível {self.carreira_info['max']}.
* **Regime Previdenciário:** **{self.n_rpps}** servidores foram identificados como contribuintes do Regime Próprio de Previdência Social (RPPS), enquanto os demais estão vinculados ao regime geral ou complementar.

###### Atributos Temporais e de Controle
O conjunto de dados preserva os atributos necessários para a simulação dinâmica, incluindo identificadores funcionais, datas de exercício corrigidas para cálculo de interstícios e siglas de cargo base. As métricas apresentadas foram extraídas em tempo real do dataframe carregado no gerenciador de estado do sistema.
"""


    def __call__(self) -> str:
        return self.markdown_content