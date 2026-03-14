from pydantic import BaseModel, field_validator, Field
import pandera.pandas as pa
from pandera.engines.pandas_engine import PydanticModel

class NivelTabela(BaseModel):

    nivel: int
    remuneracao: float
    qtd_meses_no_nivel: int = Field(gt=0)

    @field_validator('nivel')
    @classmethod
    def validar_nivel(cls, v:int)->int:

        if not isinstance(v, int):
            raise ValueError('Nivel deve ser inteiro')
        
        if v < 0:
            raise ValueError('Nivel deve ser inteiro positivo')
        
        return v
    
    @field_validator('remuneracao')
    @classmethod
    def validar_remuneracao(cls, v:float)->float:

        if not (isinstance(v, float) or isinstance(v, int)):
            raise ValueError('Remuneração deve ser numérico')
        
        if v <= 0:
            raise ValueError('Remuneração deve ser maior que zero')

        v = round(v, 2)
        
        return v

class TabelaDataframe(pa.DataFrameModel):

    class Config:
        dtype = PydanticModel(NivelTabela)
        coerce = True