from datetime import datetime, timezone
from uuid import uuid4
from fastapi import APIRouter, Body, status ,HTTPException
from pydantic import UUID4

from atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate
from atleta.models import AtletaModel
from sqlalchemy.future import select
from categorias.models import CategoriaModel
from centro_treinamento.models import CentroTreinamentoModel
from configs.dependencies import DatabaseDependency

router = APIRouter()

@router.post(path="/",
    summary="Create a new athlete",
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut
    )

async def post(
    db_session: DatabaseDependency, 
    atleta_in: AtletaIn = Body(...)
    ):
    categoria_nome = atleta_in.categoria.nome
    centro_treinamento_nome = atleta_in.centro_treinamento.nome
    ##Categoria
    categoria = (await db_session.execute(select(CategoriaModel).filter_by(nome=categoria_nome))).scalars().first()
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f'A categoria {categoria_nome} não foi encontrada.'
        )
    
    ##Centro de Treinamento
    centro_treinamento = (await db_session.execute(
    select(CentroTreinamentoModel).filter_by(nome=centro_treinamento_nome))
    ).scalars().first()
    
    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f'O centro de treinamento {centro_treinamento_nome} não foi encontrado.'
        )

    try:
        atleta_out = AtletaOut(id=uuid4(),created_at=datetime.now(timezone.utc) , **atleta_in.model_dump()) #datetime.now(timezone.utc) /datetime.utcnow()
        atleta_model = AtletaModel(**atleta_out.model_dump(exclude={'categoria', 'centro_treinamento'}))  # Exclude id and created_at to avoid conflicts
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id
        db_session.add(atleta_model)
        await db_session.commit()
    except Exception as e:
        await db_session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao adicionar atleta: {str(e.__dict__['orig']).split('\n')[0].split(': ')[-1].split('"')[0]}"
        )

    return atleta_out




# @router.post(path="/",
#              summary="Create a new atleta",
#              status_code=status.HTTP_201_CREATED,
#              response_model=AtletaOut,
#              )

# async def post(db_session: DatabaseDependency, 
#                atleta_in: AtletaIn = Body(...)
#                ) -> AtletaOut: 
#         atleta_out = AtletaOut(id=uuid4(), **atleta_in.model_dump())
#         atleta_model = AtletaModel(**atleta_out.model_dump()) 
#         db_session.add(atleta_model)
#         await db_session.commit()
        
#         return atleta_out #colocar cada um um nome diferente para não dar conflito com o nome do model



#Todos
@router.get(path=f"/",
            summary="Get all atleta by ID",
            status_code=status.HTTP_200_OK,
            response_model=list[AtletaOut],
            )

async def query(db_session: DatabaseDependency) -> list[AtletaOut]:
        atletas: list[AtletaOut] = (await db_session.execute(select(AtletaModel))).scalars().all()
        return [AtletaOut.model_validate(atleta) for atleta in atletas]





@router.get(path=f"/{id}",
            summary="Get atleta by ID",
            status_code=status.HTTP_200_OK,
            response_model=AtletaOut,
            )

async def query(id:UUID4, db_session: DatabaseDependency) -> AtletaOut:
        atleta: AtletaOut = (
                await db_session.execute(select(AtletaModel).filter_by(id=id))
                ).scalars().first()
        if not atleta:
            raise HTTPException(
                   status_code=status.HTTP_404_NOT_FOUND, 
                   detail=f"Atleta not found with id {id}",
                   )
        return atleta 


@router.patch(path=f"/{id}",
            summary="Edit atleta by ID",
            status_code=status.HTTP_200_OK,
            response_model=AtletaOut,
            )

async def query(id:UUID4, db_session: DatabaseDependency, atleta_up: AtletaUpdate = Body(...) ) -> AtletaOut:
        atleta: AtletaOut = (
                await db_session.execute(select(AtletaModel).filter_by(id=id))
                ).scalars().first()
        if not atleta:
            raise HTTPException(
                   status_code=status.HTTP_404_NOT_FOUND, 
                   detail=f"Atleta not found with id {id}",
                   )
        atleta_update = atleta.model_copy(update=atleta_up.model_dump(exclude_unset=True))
        for key, value in atleta_update.model_dump(exclude_unset=True).items():
            setattr(atleta, key, value)
        await db_session.commit()
        await db_session.refresh(atleta)
        return atleta 


@router.delete(path=f"/{id}",
            summary="Delete atleta by ID",
            status_code=status.HTTP_204_NO_CONTENT,
            )

async def query(id:UUID4, db_session: DatabaseDependency) -> None:
        atleta: AtletaOut = (
                await db_session.execute(select(AtletaModel).filter_by(id=id))
                ).scalars().first()
        if not atleta:
            raise HTTPException(
                   status_code=status.HTTP_404_NOT_FOUND, 
                   detail=f"Atleta not found with id {id}",
                   )
        await db_session.delete(atleta)
        await db_session.commit()
 