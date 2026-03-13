from ..models.simulation_step import SimulationStep
from typing import List, Callable, Generator

class SimulationCommand:

    def __init__(self)->None:

        self.steps: List[SimulationStep] = []

    def add_step(self, name:str, message:str, function:Callable)->None:

        step = SimulationStep(name=name, message=message, function=function)
        self.steps.append(step)

    def execute(self) -> Generator[SimulationStep, None, None]:
        for step in self.steps:
            # 1. Sinaliza início
            step.initialized = True
            yield step
            
            try:
                # 2. Executa a função
                step.function()
                
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