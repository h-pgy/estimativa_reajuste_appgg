import pandera.pandas as pa

schema_dados_originais = pa.DataFrameSchema(
    {
        'REGISTRO' : pa.Column(int, pa.Check(lambda x: x > 0)),
        'NOME' : pa.Column(str),
        'REF_CARGO_BAS' : pa.Column(str),
        'SIGLA' : pa.Column(str),
        'DATA_INICIO_EXERC' : pa.Column(str)
    }
)