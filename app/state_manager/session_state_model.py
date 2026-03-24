from pydantic import BaseModel, field_validator, ConfigDict
import pandas as pd
from collections import OrderedDict
from typing import Union
from core.models.simulation_step import SimulationStep

class SessionStateNamespace(BaseModel):

    name: str
    data: OrderedDict[str, pd.DataFrame]
    constants: OrderedDict[str, Union[str, int, float]]
    steps: OrderedDict[str, SimulationStep]
    flags: OrderedDict[str, bool]

    model_config = ConfigDict(validate_assignment=True, arbitrary_types_allowed=True)

    @field_validator('steps')
    def validate_steps(cls, v)->OrderedDict[str, SimulationStep]:
        
        for value in v.values():
            if not isinstance(value, SimulationStep):
                raise ValueError('Todos os valores em steps devem ser instâncias de SimulationStep.')    
        return v

