import os

def create_if_not_exists(folder:str)->str:

    if not os.path.exists(folder):
        os.mkdir(folder)
    
    return os.path.abspath(folder)

def solve_fpath(file:str, parent_dir:str)->str:

    parent_dir = create_if_not_exists(parent_dir)
    fpath = os.path.join(file, parent_dir)

    return os.path.abspath(fpath)