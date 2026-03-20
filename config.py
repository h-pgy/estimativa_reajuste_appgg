from core.utils.path import create_if_not_exists, solve_fpath, solve_dir_path
from datetime import datetime


FOLDER_DADOS = create_if_not_exists('data')
FOLDER_TABELAS = solve_dir_path('tabelas', FOLDER_DADOS)
FOLDER_STATIC = create_if_not_exists('static')

URL_SERVIDORES = 'https://dados.prefeitura.sp.gov.br/dataset/bf5df0f4-4fb0-4a5e-b013-07d098cc7b1c/resource/9fd35d06-d861-4a19-9926-a0fb3de42b50/download/verificado_ativos_03-03-2026_fev-2026in.csv'
FILE_SERVIDORES = solve_fpath('servidores.csv', FOLDER_DADOS)
ENCODING_CSV_SERVIDORES='latin1'
TABELA_ORIGINAL=solve_fpath('appgg.json', FOLDER_TABELAS)
TABELA_AMCI = solve_fpath('amci.json', FOLDER_TABELAS)
CARGO_BASE='APPGG'
DT_NOMEACAO=datetime.today()
QTD_RECEM_NOMEADOS=16
SALARIO_MINIMO=1621
VALOR_VALE_ALIMENTACAO=325.25
CONTRIBUICAO_IPREM = 0.28
ALIQUOTA_INSS = 0.21
TETO_INSS = 8475.55
ALIQUOTA_COMPLEMENTAR = 0.075