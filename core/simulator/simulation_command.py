from ..models.simulation_step import SimulationStep
import pandas as pd
from typing import List, Callable, Generator, Optional

class SimulationCommand:

    def __init__(self)->None:

        self.steps: List[SimulationStep] = []
        self.dataframe:Optional[pd.DataFrame] = None

    def add_step(self, name:str, message:str, function:Callable, args:Optional[dict]=None)->None:

        step = SimulationStep(name=name, message=message, function=function, 
                              args=args)
        self.steps.append(step)

    def solve_func_args(self, step:SimulationStep)->dict:
        func_kwargs = {}
        if step.args is not None:
            func_kwargs.update(step.args)
        return func_kwargs

    def execute(self) -> Generator[SimulationStep, None, None]:
        for step in self.steps:
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
            except Exception:
                # 3b. Sinaliza erro
                step.finished = True
                step.error = True
                yield step
                break