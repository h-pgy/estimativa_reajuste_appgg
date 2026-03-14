import json
from typing import Optional, Union
from .path import solve_fpath


def load_json(fname:str, dirname:Optional[str]=None)->Union[list, dict]:

    fpath = solve_fpath(fname, dirname)
    with open(fpath, 'r') as f:
        data = json.load(f)
    
    return data