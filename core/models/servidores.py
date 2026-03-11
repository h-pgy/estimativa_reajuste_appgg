from pydantic import BaseModel, field_validator, Field, model_validator
from datetime import datetime
from typing import Self

class ServidorBase(BaseModel):

    rf: str
    nome: str
    cargo_base: str
    secretaria: str
    nivel: int
    dt_inicio_exercicio: datetime
    rpps: bool


    @field_validator('rf')
    @classmethod
    def validar_rf(cls, v: str)->str:

        if not isinstance(v, str):
            raise ValueError('RF deve ser string')
        if not v.isdigit():
            raise ValueError('RF deve ser numérico')
        if len(v)!=7:
            raise ValueError('RF deve ter 7 digitos')

        return v

    @field_validator('nome')
    @classmethod
    def validar_nome(cls, v:str)->str:

        if not isinstance(v, str):
            raise ValueError('Nome deve ser string')
        if len(v)<1:
            raise ValueError('Nome deve ter pelo menos um caractere')
        
        return v
    
    
    @field_validator('cargo_base')
    @classmethod
    def validar_cargo_base(cls, v:str)->str:

        if not isinstance(v, str):
            raise ValueError('Cargo base deve ser string')
        if len(v)<5:
            raise ValueError('Cargo deve ter pelo menos 4 caracteres')
        
        if not v[-1].isdigit():
            raise ValueError('Cargo base deve terminar com o digito do nível')

        return v
    
    @field_validator('secretaria')
    @classmethod
    def validar_sigla_secretaria(cls, v:str)->str:

        if not isinstance(v, str):
            raise ValueError('Sigla da secretaria deve ser string')
        if len(v)<3:
            raise ValueError('Sigla da secretaria deve ter pelo menos três caracteres')
        
        return v

    @field_validator('dt_inicio_exercicio')
    @classmethod
    def validar_dt_inicio_exercicio(cls, v:datetime)->datetime:

        if not isinstance(v, datetime):
            raise ValueError('Data deve ser objeto datetime')
        
        hoje = datetime.today()

        if v > hoje:
            raise ValueError('Data deve estar no passado')
        
        if v.year < 2016:
            raise ValueError('Data deve ser no mínimo em 2016.')

        return v
    
    @field_validator('nivel')
    @classmethod
    def validar_nivel(cls, v:int)->int:

        if not isinstance(v, int):
            raise ValueError('Nivel deve ser numero inteiro')
        
        if not v > 0:
            raise ValueError('Nivel deve ser inteiro positivo')
        
        return v
    
class ServidorValores(ServidorBase):

    vencimento: float = Field(gt=0)
    decimo_terceiro: float = Field(gt=0)
    terco_ferias: float = Field(gt=0)
    vale_alimentacao: float = Field(ge=0)
    contribuicao_iprem: float = Field(ge=0)
    contribuicao_inss: float = Field(ge=0)
    previdencia_complementar: float = Field(ge=0)
    valor_total: float = Field(gt=0)

    @model_validator(mode='after')
    def verificar_contribuicoes_previdenciarias(self)-> Self:

        iprem = self.contribuicao_iprem
        inss = self.contribuicao_inss
        complementar= self.previdencia_complementar
        if iprem == 0 and inss == 0:
            raise ValueError("Deve contribuir para o IPREM ou para o INSS")
        
        if iprem > 0 and inss > 0:
            raise ValueError("Não pode contribuir para o IPREM e para o INSS ao mesmo tempo")

        if iprem > 0 and complementar > 0:
            raise ValueError("Se contribui para o IPREM não pode ter previdência complementar")


        if self.rpps and iprem <= 0:
            raise ValueError("Se é do regime próprio de previdencia (RPPS) deve contribuir para o IPREM")
        
        return self


    

    
    