from core.utils.path import create_if_not_exists, solve_fpath



FOLDER_DADOS = create_if_not_exists('data')

URL_SERVIDORES = 'https://dados.prefeitura.sp.gov.br/dataset/bf5df0f4-4fb0-4a5e-b013-07d098cc7b1c/resource/e4c65839-3bc8-4035-b0a7-108ec8740536/download/verificado_ativos_05-01-2026_dez-2025in.csv'
FILE_SERVIDORES = solve_fpath('servidores.csv', FOLDER_DADOS)