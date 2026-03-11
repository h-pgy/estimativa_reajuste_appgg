import os
import requests
from config import URL_SERVIDORES, FILE_SERVIDORES

def download_dados_servidores(fname:str=FILE_SERVIDORES, url:str=URL_SERVIDORES)->str:

    if not os.path.exists(fname):
        print('Downloading data')
        with requests.get(url) as r:
            r.raise_for_status()
            content = r.content
            with open(fname, 'wb') as f:
                f.write(content)
            
            assert os.path.exists(fname)
            return fname
    return fname