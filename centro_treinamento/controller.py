
from uuid import uuid4
from pydantic import UUID4
from sqlalchemy.future import select
from fastapi import APIRouter, Body, status, HTTPException
from centro_treinamento.models import CentroTreinamentoModel
from centro_treinamento.schemas import CentroTreinamentoIn, CentroTreinamentoOut
 
from configs.dependencies import DatabaseDependency

router = APIRouter()

@router.post(path="/",
             summary="Create a new training center",
             status_code=status.HTTP_201_CREATED,
             response_model=CentroTreinamentoOut,
             )

async def post(db_session: DatabaseDependency, 
               centro_treinamento_in: CentroTreinamentoIn = Body(...)
               ) -> CentroTreinamentoOut: 
        centro_treinamento_out = CentroTreinamentoOut(id=uuid4(), **centro_treinamento_in.model_dump())
        centro_treinamento_model = CentroTreinamentoModel(**centro_treinamento_out.model_dump()) 
        db_session.add(centro_treinamento_model)
        await db_session.commit()
        
        return centro_treinamento_out #colocar cada um um nome diferente para não dar conflito com o nome do model

#Todos
@router.get(path=f"/",
            summary="Get all training center by ID",
            status_code=status.HTTP_200_OK,
            response_model=list[CentroTreinamentoOut],
            )

async def query(db_session: DatabaseDependency) -> list[CentroTreinamentoOut]:
        centros_treinamento_out: list[CentroTreinamentoOut] = (await db_session.execute(select(CentroTreinamentoModel))).scalars().all()
        return centros_treinamento_out


@router.get(path=f"/{id}",
            summary="Get training center by ID",
            status_code=status.HTTP_200_OK,
            response_model=CentroTreinamentoOut,
            )

async def query(id:UUID4, db_session: DatabaseDependency) -> CentroTreinamentoOut:
        centro_treinamento: CentroTreinamentoOut = (
                await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id))
                ).scalars().first()
        if not centro_treinamento:
            raise HTTPException(
                   status_code=status.HTTP_404_NOT_FOUND, 
                   detail=f"Training center not found with id {id}",
                   )
        return centro_treinamento 