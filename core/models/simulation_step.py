from pydantic import BaseModel, field_validator, model_validator, ConfigDict
from typing import Callable, Self

class SimulationStep(BaseModel):

    model_config = model_config = ConfigDict(validate_assignment=True)

    name: str
    message: str
    function: Callable
    initialized: bool = False
    finished: bool = False
    sucess: bool = False
    error: bool=False

    @field_validator('name', 'message')
    @classmethod
    def validate_non_empty(cls, value)->str:
        if not value:
            raise ValueError('Value cannot be empty')
        return value

    @model_validator(mode='after')
    def validate_status_flags(self) -> Self:
        if self.finished and not self.initialized:
            raise ValueError('A step cannot be finished if it has not been initialized')
        if self.sucess and not self.finished:
            raise ValueError('A step cannot be successful if it has not been finished')
        
        if self.sucess and self.error:
            raise ValueError('A step cannot be both successful and have an error')
        
        return self
