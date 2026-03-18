from pydantic import BaseModel
import pandas as pd
from typing import List, Dict

class SessionState:

    name: str
    data: Dict[str, pd.DataFrame]
    