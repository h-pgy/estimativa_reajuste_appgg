from pydantic import BaseModel, field_validator, model_validator, ConfigDict
from typing import Callable, Self, Optional
import pandas as pd
from core.utils.str import to_snake_case

class SimulationStep(BaseModel):

    model_config = model_config = ConfigDict(validate_assignment=True, arbitrary_types_allowed=True)

    name: str
    key: str
    message: str
    function: Callable
    args: Optional[dict]=None
    result: Optional[pd.DataFrame]=None
    initialized: bool = False
    finished: bool = False
    sucess: bool = False
    error: bool=False
    error_message: Optional[str]=None

    @field_validator('name', 'message')
    @classmethod
    def validate_non_empty(cls, value)->str:
        if not value:
            raise ValueError('Value cannot be empty')
        return value

    @field_validator('key')
    @classmethod
    def key_to_snakecase(cls, value:str) -> str:
        if not isinstance(value, str):
            raise ValueError('Key must be a string')
        return to_snake_case(value)

    @model_validator(mode='after')
    def validate_status_flags(self) -> Self:
        if self.finished and not self.initialized:
            raise ValueError('A step cannot be finished if it has not been initialized')
        if self.sucess and not self.finished:
            raise ValueError('A step cannot be successful if it has not been finished')
        if self.sucess and self.result is None:
            raise ValueError('A step cannot be successful if it does not have a result')
        
        if self.sucess and self.error:
            raise ValueError('A step cannot be both successful and have an error')
        
        if self.error and not self.error_message:
            raise ValueError('A step cannot have an error without an error message')
        
        return self

    @property
    def current_status(self)->str:
        if self.error:
            return 'error'
        elif self.sucess:
            return 'success'
        elif self.finished:
            return 'finished'
        elif self.initialized:
            return 'initialized'
        else:
            return 'not started'
