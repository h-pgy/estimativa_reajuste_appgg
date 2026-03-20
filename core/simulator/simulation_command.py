from ..models.simulation_step import SimulationStep
from collections import OrderedDict
import pandas as pd
from typing import List, Callable, Generator, Optional

class SimulationCommand:

    def __init__(self, name:str, initial_df:Optional[pd.DataFrame]=None)->None:

        self.name = name
        self.steps: OrderedDict[str, SimulationStep] = OrderedDict()
        self.dataframe:Optional[pd.DataFrame] = initial_df

    def add_step(self, name:str, key:str, message:str, function:Callable, args:Optional[dict]=None)->None:

        if key in self.steps:
            raise ValueError(f'Chave {key} já existente nos steps.')
        step = SimulationStep(name=name, key=key, message=message, function=function, 
                              args=args)
        self.steps[key] = step

    def get_step(self, key:str)->SimulationStep:

        if key not in self.steps:
            raise ValueError(f'Step com a key {key} não existente')
        
        return self.steps[key]
    
    @property
    def num_steps(self)->int:
        return len(self.steps)

    def solve_func_args(self, step:SimulationStep)->dict:
        func_kwargs = {}
        if step.args is not None:
            func_kwargs.update(step.args)
        return func_kwargs

    def execute(self) -> Generator[SimulationStep, None, None]:
        for key, step in self.steps.items():
            # 1. Sinaliza início
            step.initialized = True
            yield step
            
            try:
                # 2. Executa a função
                func_kwargs = self.solve_func_args(step)
                self.dataframe = step.function(df=self.dataframe, **func_kwargs)
                step.result = self.dataframe
                
                # 3. Sinaliza sucesso (o validator garante a ordem)
                step.finished = True
                step.sucess = True
                yield step
            except Exception as e:
                # 3b. Sinaliza erro
                step.finished = True
                step.error_message = "Error: {}. Message: {}".format(type(e).__name__, str(e))
                step.error = True
                raise e
                yield step
                break