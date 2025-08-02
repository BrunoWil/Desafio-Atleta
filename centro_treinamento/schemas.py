from pydantic import UUID4, Field
from typing import Annotated
from contrib.schemas import BaseSchema

class CentroTreinamentoIn(BaseSchema):
    nome: Annotated[str, Field(..., description="Nome do Centro de Treinamento", examples=["Club Ce"], max_length=20)]
    endereco: Annotated[str, Field(..., description="Endereço do Centro de Treinamento", examples=["Rua das Flores, 123"], max_length=60)]
    proprietario: Annotated[str, Field(..., description="Nome do Proprietário do Centro de Treinamento", examples=["Maria Oliveira"], max_length=30)]

class CentroTreinamentoAtleta(CentroTreinamentoIn):
    nome: Annotated[str, Field(..., description="ID da Centro de Treinamento",examples=["Club Ce"], max_length=20)]
    pass

class CentroTreinamentoOut(CentroTreinamentoIn):
    id: Annotated[UUID4, Field(..., description="ID da Centro Treinamento")]
    pass