

from time import timezone
from contrib.models import BaseModel
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Float, Integer, String, DateTime, ForeignKey
from datetime import datetime


class AtletaModel(BaseModel):
        __tablename__ = 'atletas'
        pk_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
        nome: Mapped[str] = mapped_column(String(50), nullable=False)
        cpf: Mapped[str] = mapped_column(String(14), nullable=False, unique=True)
        idade: Mapped[int] = mapped_column(Integer, nullable=False)
        peso: Mapped[float] = mapped_column(Float,nullable=False)
        altura: Mapped[float] = mapped_column(Float,nullable=False)
        sexo: Mapped[str] = mapped_column(String(1), nullable=False)
        # created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
        created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
        categoria: Mapped['CategoriaModel'] = relationship(back_populates="atleta", lazy='selectin')
        categoria_id : Mapped[int] = mapped_column(ForeignKey('categorias.pk_id'))
        centro_treinamento: Mapped['CentroTreinamentoModel'] = relationship(back_populates="atleta", lazy='selectin')
        centro_treinamento_id : Mapped[int] = mapped_column(ForeignKey('centros_treinamento.pk_id'))

from categorias.models import CategoriaModel  # Import here to avoid circular import issues
from centro_treinamento.models import CentroTreinamentoModel  # Import here to avoid circular