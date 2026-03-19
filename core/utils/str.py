import re

def to_snake_case(string:str)->str:

    return re.sub(r'(?<!^)(?=[A-Z])', '_', string).lower()