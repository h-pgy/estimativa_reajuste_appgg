from pydantic import BaseModel
from typing import Callable, Any

class ComponentItem(BaseModel):

    args: list = []
    kwargs: dict[str,Any] = {}
    write_func: Callable
