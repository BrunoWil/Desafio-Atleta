from contrib.models import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String


class CategoriaModel(BaseModel):
        __tablename__ = 'categorias'
        pk_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
        nome: Mapped[str] = mapped_column(String(10), nullable=False,unique=True)
        atleta: Mapped['AtletaModel'] = relationship(back_populates="categoria")

from atleta.models import AtletaModel #import here to avoid circular import issues   
#   