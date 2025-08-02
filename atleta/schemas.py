from pydantic import Field, PositiveFloat
from typing import Annotated, Optional
from categorias.schemas import CategoriaIn
from centro_treinamento.schemas import CentroTreinamentoAtleta
from contrib.schemas import BaseSchema, OutMixin

class Atleta(BaseSchema):
    nome: Annotated[str, Field(..., description="Nome do atleta", examples=["João Silva"], max_length=50)]
    cpf: Annotated[str, Field(..., description="CPF do atleta", examples=["123.456.789-00"], max_length=14)]
    idade: Annotated[int, Field(..., description="Idade do atleta", examples=[25], ge=0)]
    peso: Annotated[PositiveFloat, Field(..., description="Peso do atleta em quilogramas", examples=[70.0])]
    altura: Annotated[PositiveFloat, Field(..., description="Altura do atleta em metros", examples=[1.75])]
    sexo: Annotated[str, Field(..., description="Sexo do atleta", examples=["M", "F"], max_length=1)]
    categoria: Annotated[CategoriaIn, Field(description='Categoria do atleta')]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description='Centro de treinamento do atleta')]

class AtletaIn(Atleta):
    pass
    
class AtletaOut(Atleta,OutMixin):
    pass

class AtletaUpdate(BaseSchema):
    nome: Annotated[Optional[str], Field(None, description='Nome do atleta', example=['Joao'], max_length=50)]
    idade: Annotated[Optional[int], Field(None, description='Idade do atleta', example=[25], ge=0)]