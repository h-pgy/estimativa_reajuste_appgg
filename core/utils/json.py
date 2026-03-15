import json
from typing import Optional, Union
import pandas as pd
from .path import solve_fpath


def load_json(fname:str, dirname:Optional[str]=None)->Union[list, dict]:

    fpath = solve_fpath(fname, dirname)
    with open(fpath, 'r') as f:
        data = json.load(f)
    
    return data

def load_json_to_dataframe(fname:str, dirname:Optional[str]=None)->pd.DataFrame:

    data = load_json(fname, dirname)
    if type(data) is not list:
        raise ValueError('Expected a list of dictionaries to convert to DataFrame')
    return pd.DataFrame(data)