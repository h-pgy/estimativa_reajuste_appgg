import os
from typing import Optional

def create_if_not_exists(folder:str)->str:

    if not os.path.exists(folder):
        os.mkdir(folder)
    
    return os.path.abspath(folder)

def solve_fpath(file:str, parent_dir:Optional[str]=None)->str:

    if parent_dir is not None:
        parent_dir = create_if_not_exists(parent_dir)
        file = os.path.join(parent_dir, file)

    return os.path.abspath(file)