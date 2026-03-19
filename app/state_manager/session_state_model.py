from pydantic import BaseModel, field_validator, ConfigDict
import pandas as pd
from typing import List, Dict

class SessionStateNamespace(BaseModel):

    name: str
    data: Dict[str, pd.DataFrame]
    steps: List[str]
    flags: Dict[str, bool]

    model_config = ConfigDict(validate_assignment=True)

    @field_validator('steps')
    def validate_steps(cls, v)->List[str]:
        if not isinstance(v, list):
            raise ValueError('Steps deve ser uma lista de strings.')
        
        #checa se há duplicados
        if len(set(v)) != len(v):
            raise ValueError('Steps não pode conter valores duplicados.')
        
        return v

