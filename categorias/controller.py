
from uuid import uuid4
from pydantic import UUID4
from sqlalchemy.future import select
from fastapi import APIRouter, Body, status, HTTPException
from categorias.models import CategoriaModel
from categorias.schemas import CategoriaIn, CategoriaOut
 
from configs.dependencies import DatabaseDependency

router = APIRouter()

@router.post(path="/",
             summary="Create a new category",
             status_code=status.HTTP_201_CREATED,
             response_model=CategoriaOut,
             )

async def post(db_session: DatabaseDependency, 
               categoria_in: CategoriaIn = Body(...)
               ) -> CategoriaOut: 
        categoria_out = CategoriaOut(id=uuid4(), **categoria_in.model_dump())
        categoria_model = CategoriaModel(**categoria_out.model_dump()) 
        db_session.add(categoria_model)
        await db_session.commit()
        
        return categoria_out

#Todos
@router.get(path=f"/",
            summary="Get all category by ID",
            status_code=status.HTTP_200_OK,
            response_model=list[CategoriaOut],
            )

async def query(db_session: DatabaseDependency) -> list[CategoriaOut]:
        categorias: list[CategoriaOut] = (await db_session.execute(select(CategoriaModel))).scalars().all()
        return categorias


@router.get(path=f"/{id}",
            summary="Get category by ID",
            status_code=status.HTTP_200_OK,
            response_model=CategoriaOut,
            )

async def query(id:UUID4, db_session: DatabaseDependency) -> CategoriaOut:
        categoria: CategoriaOut = (
                await db_session.execute(select(CategoriaModel).filter_by(id=id))
                ).scalars().first()
        if not categoria:
            raise HTTPException(
                   status_code=status.HTTP_404_NOT_FOUND, 
                   detail=f"Category not found with id {id}",
                   )
        return categoria 